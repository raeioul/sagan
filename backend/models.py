from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    spouse_name = db.Column(db.String(200))
    dob = db.Column(db.Date, nullable=False)
    spouse_dob = db.Column(db.Date)
    last_four_ssn = db.Column(db.String(4), nullable=False)
    spouse_last_four_ssn = db.Column(db.String(4))
    monthly_salary = db.Column(db.Float, default=0)
    spouse_monthly_salary = db.Column(db.Float, default=0)
    agreed_expense_budget = db.Column(db.Float, default=0)
    private_reserve_target = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    deductibles = db.relationship('InsuranceDeductible', backref='client', lazy=True, cascade='all, delete-orphan')
    accounts = db.relationship('Account', backref='client', lazy=True, cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='client', lazy=True, cascade='all, delete-orphan')

    @property
    def age(self):
        today = datetime.utcnow().date()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))

    @property
    def spouse_age(self):
        if not self.spouse_dob:
            return None
        today = datetime.utcnow().date()
        return today.year - self.spouse_dob.year - ((today.month, today.day) < (self.spouse_dob.month, self.spouse_dob.day))

    @property
    def total_inflow(self):
        return (self.monthly_salary or 0) + (self.spouse_monthly_salary or 0)

    @property
    def automated_transfer(self):
        return self.total_inflow - (self.agreed_expense_budget or 0)

    @property
    def calculated_private_reserve_target(self):
        total_deductibles = sum(d.amount for d in self.deductibles)
        return (6 * (self.agreed_expense_budget or 0)) + total_deductibles

    @property
    def last_report_date(self):
        if not self.reports:
            return None
        return max(r.created_at for r in self.reports)

    @property
    def last_report_quarter(self):
        if not self.reports:
            return None
        return max(self.reports, key=lambda r: r.created_at).quarter


class InsuranceDeductible(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    label = db.Column(db.String(200), nullable=False) # e.g. "Health", "Auto"
    amount = db.Column(db.Float, default=0)


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    # Types: 'retirement_client1', 'retirement_client2', 'non_retirement', 'trust', 'liability'
    account_type = db.Column(db.String(50), nullable=False)
    owner = db.Column(db.String(50), nullable=False) # 'client1', 'client2', 'joint', 'trust'
    name = db.Column(db.String(200), nullable=False)
    last_four = db.Column(db.String(4))
    interest_rate = db.Column(db.Float) # mainly for liabilities
    is_liability = db.Column(db.Boolean, default=False)
    property_address = db.Column(db.String(300)) # for trust accounts


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    quarter = db.Column(db.String(10), nullable=False) # e.g. "2026-Q2"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Hardcoded or snapshot properties at the time of report generation
    inflow_balance = db.Column(db.Float, default=0)
    outflow_balance = db.Column(db.Float, default=0)
    private_reserve_balance = db.Column(db.Float, default=0)
    schwab_brokerage_balance = db.Column(db.Float, default=0)
    target_amount = db.Column(db.Float, default=0)

    # Relationships
    balances = db.relationship('AccountBalance', backref='report', lazy=True, cascade='all, delete-orphan')


class AccountBalance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    balance = db.Column(db.Float, default=0)
    cash_balance = db.Column(db.Float) # for investment/brokerage accounts, to show cash portion

    # Relationship to access the original account metadata
    account = db.relationship('Account', backref=db.backref('balances', lazy=True, cascade='all, delete-orphan'))
