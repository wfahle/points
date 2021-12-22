#!/usr/bin/python
# app.py
import json
from urllib import parse
from datetime import datetime
from flask import Flask, request, jsonify
from flask import g, session
from flask_openid import OpenID

app = Flask(__name__)
oid = OpenID(app, '/dev/points/oidpath', safe_roots=[])

#unordered list of transactions
points = [
]

@app.before_request
def lookup_current_user():
    g.user = None
    if 'openid' in session:
        openid = session['openid']
        g.user = User.query.filter_by(openid=openid).first()

@app.get("/clear")
def clear(): # clear all transactions
    points.clear()
    return jsonify("")

@app.get("/transactions")
def get_transactions(): # get transactions in order currently known
    respts = sorted(points, key=lambda x: x['timestamp'])
    return jsonify(respts)

@app.get("/totals") # get total point count by payer
def get_totals():
    totals = {}
    for transaction in points:
        #total points per payer dictionary
        if transaction['payer'] in totals:
            totals[transaction['payer']]+=transaction['points']
        else:
            totals[transaction['payer']]=transaction['points']
    return jsonify(totals)

@app.get("/points") # get current points for user - a real version of this would expect a user ID 
                    # and have a dictionary of transactions per user
def get_points():
    total = 0
    for transaction in points:
        total = total + transaction['points']
    return jsonify(total)

def negative_transaction(trans, payer, amount): # resolve a transaction with negative points as if it were a spend
    # select items from points that have a payer value of payer
    bypayer = [t for t in trans if t['payer'] == payer]
    # get all other transactions that were not this payer
    notpayer = [t for t in trans if t['payer'] != payer]
    # sort the resulting list so that the oldest is first
    res = sorted(bypayer, key=lambda x: x['timestamp'])
    # amount is assumed to be negative, reverse it
    amount = -amount
    while amount > 0:
        if len(res) < 1:
            return trans # no transactions exist, ignore
        pts = res[0]['points']
        if pts > amount:
            res[0]['points'] = pts - amount
            amount = 0
        else:
            amount -= pts
            if len(res) == 1:
                res[0]['points'] = 0 # keep around payers even if there are 0 points
                amount = 0 # there are no other transactions to get from for this payer, ignore remaining negative points
            else:
                del res[0] #if there's another transaction still for this payer, remove the empty one
    # add remaining transactions back to nonpayer list, result is all remaining transactions
    notpayer += res
    return sorted(notpayer, key=lambda x: x['timestamp'])

@app.post("/spend")
def spend_points():
    global points
    if request.is_json:
        # note - when we go to spend points, we resolve the transactions we have; later calls obviously can't be used in spend
        spend = parse.parse_qs(str(request.data, encoding='utf-8'))
        # note - full implementation would sanitize inputs here
        amount = int(spend['points'][0])
        # sort current transactions into timestamp order
        respts = sorted(points, key=lambda x: x['timestamp'])
        # get positive transactions
        pos = [t for t in respts if t['points'] > 0]
        # get zero or negative transactions
        neg = [t for t in respts if t['points'] <= 0]
        for t in neg:
            pos = negative_transaction(pos,t['payer'],t['points'])
        res = pos
        # dictionary to keep spend account by payer - transactions are updated to match
        out = {}
        # will repopulate when finished
        if len(res) < 1:
            return out, 400 # no transactions exist, ignore
        points.clear()
        idx = 0
        while amount > 0 and idx < len(res):
            pts = res[idx]['points']
            payer = res[idx]['payer']
            spent = 0
            if pts > amount:
                res[idx]['points'] = pts - amount
                spent=-amount
                amount = 0
            else:
                spent=-pts
                amount -= pts
                res[idx]['points'] = 0
            if payer in out:
                out[payer] += spent
            else:
                out[payer] = spent
            idx+=1

        # remove duplicate zero transactions - keep them if there are no others of that payer
        zer = [t for t in res if t['points'] == 0]
        pos = [t for t in res if t['points'] > 0]
        for z in zer:
            found = False
            for p in pos:
                if p['payer'] == z['payer']:
                    found = True
            if not found:
                pos.append(z)
        # add remaining transactions back to transaction list
        if len(pos) > 0:
            points = pos
        return out, 201
    return {"error": "Request must be JSON"}, 415

@app.post("/transaction")
def add_points():
    if request.is_json:
        transaction = parse.parse_qs(str(request.data, encoding='utf-8'))
        # convert from lists to single entities
        # note - full implementation would sanitize inputs here
        transaction['payer']=transaction['payer'][0]
        transaction['points'] = int(transaction['points'][0])
        timestamp=transaction['timestamp'][0]
        timestamp=timestamp.replace('Z','+00:00')
        transaction['timestamp']=datetime.fromisoformat(timestamp)
        #add to list of transactions
        points.append(transaction)
        return transaction, 201
    return {"error": "Request must be JSON"}, 415

if __name__ == "__main__":
    app.run()
