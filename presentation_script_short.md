# AW Client Report Portal — Presentation Script (Short)

---

## 1. The Problem

"The firm has 3 people — Andrew, Rebecca, Maryann — and 6 clients on retainer. Every quarter, they manually pull balances from Pinnacle Bank (via email), Schwab, Zillow, and RightCapital, then assemble everything by hand in Canva and Word. It takes a full day per client. Rebecca: *'all that math is done manually, automating that would be great.'* Maryann: *'This takes us a day. If we could take this down to an hour.'*"

## 2. What We Built

"A portal that:

1. Stores client profiles once — names, DOB, salaries, accounts, deductibles
2. Shows a structured form pre-filled with static data, auto-calculates everything
3. Generates pixel-perfect SACS (cashflow) and TCC (net worth) PDFs with one click"

## 3. Dashboard

"All clients at a glance with name, spouse, age, inflow, expense budget, and last report date. From here: edit profile, generate a new report, or re-download past PDFs."

## 4. Adding a Client

"Enter static data once: client & spouse info (name, DOB, SSN, salary), expense budget, insurance deductibles, and account structure — retirement per spouse, non-retirement, trust with property address, liabilities with interest rates. Set once, reused every quarter."

## 5. Generating a Report

"A pre-meeting checklist reminds the team to request bank balances and check Zillow. Then enter the quarterly numbers:

- Inflow and outflow pre-filled but adjustable — surplus calculates in real time
- Private Reserve and Schwab balances
- Every account gets a balance field with last quarter's value and a 'Use Last' button

Missing fields are highlighted in red. A real-time TCC summary shows retirement totals, net worth, and liabilities updating as you type."

## 6. The PDFs

**SACS** (2 pages):
- Page 1: Green Inflow Hub → Red Outflow Hub → Blue Private Reserve, with arrows and monthly amounts
- Page 2: FICA safety cap vs Investment account, automated rebalancing, full target calculation breakdown

**TCC** (1 page):
- Client info badges with DOB, age, SSN
- Retirement totals per spouse, non-retirement, trust with property address
- Grand total net worth
- Liabilities table (tracked separately, not subtracted from net worth)

Both PDFs are fixed-layout, print-ready, no alignment issues.

## 7. What's Next

"V2 could add auto-pull from RightCapital, Schwab, and Zillow. Canva export and Dropbox auto-save are optional add-ons discussed but deferred. The core need is solved: what took a full day now takes 30 minutes with zero math errors."
