# AW Client Report Portal — Presentation Script

---

## Slide 1: The Problem

**Script:**

"Andrew, Rebecca, and Maryann run a financial planning firm in Atlanta serving high-net-worth families. They have about six clients on retainer with quarterly meetings.

Every quarter, the process goes like this:

- Maryann emails Pinnacle Bank to request account balances — comes back via secure email.
- Rebecca logs into Schwab directly and pulls investment balances.
- Someone checks Zillow for the latest home value.
- They open RightCapital or dig through client statements.

Then all that data gets manually copied into a Canva template or a Word document. Every number is manually added, subtracted, cross-referenced. Rebecca told us: *'all of that math is done manually, so even just automating that would be great.'* Maryann said: *'This takes us a day to prepare. If we could take this down to an hour.'*

That's the problem — a full day of manual work, prone to errors, every single quarter per client."

---

## Slide 2: What We Built

**Script:**

"We built a portal that does three things:

1. **Stores client profiles once** — names, DOB, salaries, expense budgets, account structures, insurance deductibles. No more re-entering the same info every quarter.

2. **Structured data entry with automatic math** — a form with every field they need, pre-populated with the static data from the profile. They enter the dynamic quarterly balances, and everything is calculated instantly: inflow minus outflow, retirement totals per spouse, net worth, liabilities. No manual addition, no spreadsheets.

3. **Pixel-perfect PDF reports** — two PDFs that match exactly what Andrew created: the SACS cashflow diagram and the TCC net worth chart. One click to download.

Let me show you how it works."

---

## Slide 3: Demo — Client Dashboard

**Script:**

"Here's the main dashboard. You can see all your clients at a glance — name, spouse, age, monthly inflow, expense budget, and the **last report date** so you know when each client was last updated.

From here you can:

- Click **Profile Settings** to edit a client's static info
- Click **Generate Report** to start a new quarterly report
- Click the **past reports dropdown** to re-download any previous quarter's PDFs

And the **Add Client** button in the top right to onboard someone new."

---

## Slide 4: Demo — Adding a Client

**Script:**

"When you add a new client, you enter their static information once.

- **Client 1** and **Client 2** (spouse) — names, DOB, last four of SSN, monthly salary
- **SACS settings** — the agreed monthly expense budget and private reserve target
- **Insurance deductibles** — health, auto, etc. These automatically feed into the FICA safety cap calculation
- **Account structures** — every account the client has: retirement accounts per spouse, non-retirement accounts, trust/property accounts with the **property address** for Zillow lookups, and liabilities with interest rates

All of this is set once and re-used every quarter. No more hunting through Dropbox folders and Excel files."

---

## Slide 5: Demo — Generating a Report

**Script:**

"When it's time to prepare for a quarterly meeting, click **Generate Report** for any client.

The page is organized in sections:

**Step 1: Pre-Meeting Checklist** — reminders of what to do two days before:
- Request the Private Reserve balance from Pinnacle Bank via email
- Retrieve Schwab brokerage balances
- Look up the Zillow Zestimate for the trust property

**Step 2: SACS Cashflow Data** — enter the quarterly numbers:
- Monthly inflow and outflow — pre-filled from the client's profile but adjustable
- The surplus is calculated **in real-time**: inflow minus outflow
- Private Reserve and Schwab brokerage current balances

**Step 3: TCC Account Balances** — every configured account appears with its balance field. Each field shows the **last quarter's value** with a handy **'Use Last' button** if nothing changed.

And now the new addition: a **real-time TCC Net Worth Summary** at the bottom — as you type in account balances, you can see Client 1 retirement, Client 2 retirement, non-retirement, trust, grand total, and liabilities updating instantly.

Fields that haven't been filled yet are highlighted in red so you never miss a number."

---

## Slide 6: Demo — The Reports

**Script:**

"Once you submit, you land on the report summary page. Here you can:

- **Download SACS PDF** — the Simple Automated Cash Flow System diagram
- **Download TCC PDF** — the Total Client Chart net worth overview

**The SACS PDF has two pages:**

Page 1 shows the cashflow flow diagram: the green Inflow Hub with the monthly income, the red Outflow Hub with expenses and the automated transfer arrow labeled 'Auto Transfer on the 28th,' the blue Private Reserve with the surplus flowing in, and a system logic legend at the bottom explaining how everything works.

Page 2 shows the magnified Private Reserve view — the FICA Account (safety net) with its target cap and funding status, the Investment Account (Schwab), the automated rebalancing arrow between them, and a detailed calculation breakdown of the target cap.

**The TCC PDF shows:**

- Green info badges for each spouse with DOB, age, and last four SSN
- Client 1 retirement accounts and total
- Client 2 retirement accounts and total
- Non-retirement joint accounts and total
- Trust and property assets with the property address
- Grand total net worth
- Liabilities tracked separately with type, interest rate, and balance

All numbers are in the right places. Nothing shifts. Nothing misaligns. Print-ready, client-presentation quality."

---

## Slide 7: Tech Stack Summary

**Script:**

"Just to give you a quick look under the hood:

- **Frontend:** Plain HTML, CSS, and JavaScript — no framework overhead. The team is three people, it needs to be simple and fast.
- **Backend:** Python with Flask — handles the form processing, all the calculations, and database operations.
- **Database:** SQLite — six clients, minimal volume, no need for a heavy database server. Runs on Railway.
- **PDF Generation:** ReportLab — generates pixel-perfect, fixed-layout PDFs that match the existing SACS and TCC templates exactly.
- **Hosting:** Railway — standard Sagan deployment.

No AI, no API integrations in V1. All data is entered manually by the team, as requested. V2 can add automated pulls from RightCapital, Schwab, and Zillow if needed."

---

## Slide 8: What's Next

**Script:**

"A few things that came up in the conversations that we discussed but didn't build into V1:

- **Canva export:** Exporting directly to Canva for last-minute visual adjustments was proposed. PDF download covers the core need, but this can be added.
- **Dropbox auto-save:** Automatically saving generated reports to the client's Dropbox folder.
- **Auto-pull from RightCapital, Schwab, and Zillow:** Deferred to V2 — data reliability and compliance concerns need more investigation.

The portal as it stands today takes what was a full-day manual process and turns it into a 30-minute data entry session with one-click PDF generation. No more manual math errors. No more re-entering the same data every quarter. No more alignment issues in Canva."

---

## Q&A

**Script:**

"Happy to take any questions — or if you want, I can walk through a live demo right now."
