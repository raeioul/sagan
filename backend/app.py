import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-sagan')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///' + os.path.join(os.path.dirname(__file__), '..', 'data', 'portal.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure data directory exists
os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'data'), exist_ok=True)

from models import db, Client, Account, Report, AccountBalance, InsuranceDeductible
db.init_app(app)

with app.app_context():
    db.create_all()

from pdf_generator import generate_sacs_pdf, generate_tcc_pdf

@app.template_filter('numberformat')
def numberformat_filter(value):
    if value is None:
        return '0'
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return str(value)

@app.route('/')
def index():
    clients = Client.query.order_by(Client.name).all()
    return render_template('index.html', clients=clients)

@app.route('/client/new', methods=['GET', 'POST'])
def client_new():
    if request.method == 'POST':
        # Retrieve client info
        client = Client(
            name=request.form['name'],
            spouse_name=request.form.get('spouse_name') or None,
            dob=datetime.strptime(request.form['dob'], '%Y-%m-%d').date(),
            spouse_dob=datetime.strptime(request.form['spouse_dob'], '%Y-%m-%d').date() if request.form.get('spouse_dob') else None,
            last_four_ssn=request.form['last_four_ssn'],
            spouse_last_four_ssn=request.form.get('spouse_last_four_ssn') or None,
            monthly_salary=float(request.form.get('monthly_salary') or 0),
            spouse_monthly_salary=float(request.form.get('spouse_monthly_salary') or 0),
            agreed_expense_budget=float(request.form.get('agreed_expense_budget') or 0),
            private_reserve_target=float(request.form.get('private_reserve_target') or 0),
        )
        db.session.add(client)
        db.session.flush()

        # Retrieve accounts info
        account_names = request.form.getlist('account_name[]')
        account_types = request.form.getlist('account_type[]')
        account_owners = request.form.getlist('account_owner[]')
        account_last_fours = request.form.getlist('account_last_four[]')
        account_interest_rates = request.form.getlist('account_interest_rate[]')
        account_property_addresses = request.form.getlist('account_property_address[]')

        for i in range(len(account_names)):
            if account_names[i].strip():
                is_liab = (account_types[i] == 'liability')
                rate = float(account_interest_rates[i]) if account_interest_rates[i] and not is_liab else (float(account_interest_rates[i]) if account_interest_rates[i] else None)
                addr = account_property_addresses[i].strip() if i < len(account_property_addresses) and account_property_addresses[i].strip() else None
                acc = Account(
                    client_id=client.id,
                    name=account_names[i],
                    account_type=account_types[i],
                    owner=account_owners[i],
                    last_four=account_last_fours[i] or None,
                    interest_rate=rate,
                    is_liability=is_liab,
                    property_address=addr
                )
                db.session.add(acc)

        # Retrieve insurance deductibles info
        deductible_labels = request.form.getlist('deductible_label[]')
        deductible_amounts = request.form.getlist('deductible_amount[]')

        for i in range(len(deductible_labels)):
            if deductible_labels[i].strip():
                ded = InsuranceDeductible(
                    client_id=client.id,
                    label=deductible_labels[i],
                    amount=float(deductible_amounts[i]) if deductible_amounts[i] else 0
                )
                db.session.add(ded)

        # Re-calculate target based on actual monthly expense budget and deductibles if not set manually
        total_ded = sum(float(a) for a in deductible_amounts if a)
        calculated_target = 6 * client.agreed_expense_budget + total_ded
        if not client.private_reserve_target or client.private_reserve_target == 0:
            client.private_reserve_target = calculated_target

        db.session.commit()
        flash('Client created successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('client_form.html', client=None)

@app.route('/client/<int:id>/edit', methods=['GET', 'POST'])
def client_edit(id):
    client = db.session.get(Client, id)
    if not client:
        flash('Client not found.', 'error')
        return redirect(url_for('index'))

    if request.method == 'POST':
        client.name = request.form['name']
        client.spouse_name = request.form.get('spouse_name') or None
        client.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        client.spouse_dob = datetime.strptime(request.form['spouse_dob'], '%Y-%m-%d').date() if request.form.get('spouse_dob') else None
        client.last_four_ssn = request.form['last_four_ssn']
        client.spouse_last_four_ssn = request.form.get('spouse_last_four_ssn') or None
        client.monthly_salary = float(request.form.get('monthly_salary') or 0)
        client.spouse_monthly_salary = float(request.form.get('spouse_monthly_salary') or 0)
        client.agreed_expense_budget = float(request.form.get('agreed_expense_budget') or 0)
        client.private_reserve_target = float(request.form.get('private_reserve_target') or 0)

        # Retrieve accounts info
        account_ids = request.form.getlist('account_id[]')
        account_names = request.form.getlist('account_name[]')
        account_types = request.form.getlist('account_type[]')
        account_owners = request.form.getlist('account_owner[]')
        account_last_fours = request.form.getlist('account_last_four[]')
        account_interest_rates = request.form.getlist('account_interest_rate[]')
        account_property_addresses = request.form.getlist('account_property_address[]')

        submitted_account_ids = []
        for i in range(len(account_names)):
            if account_names[i].strip():
                is_liab = (account_types[i] == 'liability')
                rate = float(account_interest_rates[i]) if account_interest_rates[i] else None
                addr = account_property_addresses[i].strip() if i < len(account_property_addresses) and account_property_addresses[i].strip() else None
                
                acc_id = account_ids[i] if i < len(account_ids) else ""
                if acc_id:
                    # Update existing account
                    acc = db.session.get(Account, int(acc_id))
                    if acc and acc.client_id == client.id:
                        acc.name = account_names[i]
                        acc.account_type = account_types[i]
                        acc.owner = account_owners[i]
                        acc.last_four = account_last_fours[i] or None
                        acc.interest_rate = rate
                        acc.is_liability = is_liab
                        acc.property_address = addr
                        submitted_account_ids.append(acc.id)
                else:
                    # Create new account
                    acc = Account(
                        client_id=client.id,
                        name=account_names[i],
                        account_type=account_types[i],
                        owner=account_owners[i],
                        last_four=account_last_fours[i] or None,
                        interest_rate=rate,
                        is_liability=is_liab,
                        property_address=addr
                    )
                    db.session.add(acc)
                    db.session.flush()
                    submitted_account_ids.append(acc.id)

        # Delete removed accounts
        for acc in client.accounts:
            if acc.id not in submitted_account_ids:
                db.session.delete(acc)

        # Retrieve insurance deductibles info
        deductible_ids = request.form.getlist('deductible_id[]')
        deductible_labels = request.form.getlist('deductible_label[]')
        deductible_amounts = request.form.getlist('deductible_amount[]')

        submitted_deductible_ids = []
        for i in range(len(deductible_labels)):
            if deductible_labels[i].strip():
                amount = float(deductible_amounts[i]) if deductible_amounts[i] else 0
                ded_id = deductible_ids[i] if i < len(deductible_ids) else ""
                
                if ded_id:
                    # Update existing
                    ded = db.session.get(InsuranceDeductible, int(ded_id))
                    if ded and ded.client_id == client.id:
                        ded.label = deductible_labels[i]
                        ded.amount = amount
                        submitted_deductible_ids.append(ded.id)
                else:
                    # Create new
                    ded = InsuranceDeductible(
                        client_id=client.id,
                        label=deductible_labels[i],
                        amount=amount
                    )
                    db.session.add(ded)
                    db.session.flush()
                    submitted_deductible_ids.append(ded.id)

        # Delete removed deductibles
        for ded in client.deductibles:
            if ded.id not in submitted_deductible_ids:
                db.session.delete(ded)

        # Re-calculate target based on budget and deductibles if not manual or set to 0
        total_ded = sum(float(a) for a in deductible_amounts if a)
        calculated_target = 6 * client.agreed_expense_budget + total_ded
        if not client.private_reserve_target or client.private_reserve_target == 0:
            client.private_reserve_target = calculated_target

        db.session.commit()
        flash('Client updated successfully.', 'success')
        return redirect(url_for('index'))

    return render_template('client_form.html', client=client)

@app.route('/client/<int:id>/delete', methods=['POST'])
def client_delete(id):
    client = db.session.get(Client, id)
    if client:
        db.session.delete(client)
        db.session.commit()
        flash('Client deleted successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/client/<int:id>/report/new', methods=['GET', 'POST'])
def report_new(id):
    client = db.session.get(Client, id)
    if not client:
        flash('Client not found.', 'error')
        return redirect(url_for('index'))

    # Retrieve last report if any, to prefill values
    last_report = Report.query.filter_by(client_id=client.id).order_by(Report.created_at.desc()).first()

    if request.method == 'POST':
        quarter = request.form['quarter']
        report = Report(
            client_id=client.id,
            quarter=quarter,
            inflow_balance=float(request.form.get('inflow_balance') or 0),
            outflow_balance=float(request.form.get('outflow_balance') or 0),
            private_reserve_balance=float(request.form.get('private_reserve_balance') or 0),
            schwab_brokerage_balance=float(request.form.get('schwab_brokerage_balance') or 0),
            target_amount=float(request.form.get('target_amount') or 0)
        )
        db.session.add(report)
        db.session.flush()

        # Save individual account balances
        for acc in client.accounts:
            val_name = f'account_balance_{acc.id}'
            cash_name = f'account_cash_{acc.id}'
            balance_val = float(request.form.get(val_name) or 0)
            cash_val = float(request.form.get(cash_name)) if request.form.get(cash_name) else None
            
            ab = AccountBalance(
                report_id=report.id,
                account_id=acc.id,
                balance=balance_val,
                cash_balance=cash_val
            )
            db.session.add(ab)

        db.session.commit()
        flash('Quarterly report generated.', 'success')
        return redirect(url_for('report_view', id=report.id))

    # Pre-calculated default target for this report
    default_target = client.calculated_private_reserve_target
    
    # Compute auto-quarter string: e.g. "2026-Q2"
    now = datetime.utcnow()
    q_str = f"{now.year}-Q{(now.month - 1) // 3 + 1}"

    # Prepare historical references dictionary
    prev_balances = {}
    if last_report:
        for bal in last_report.balances:
            prev_balances[bal.account_id] = {
                'balance': bal.balance,
                'cash_balance': bal.cash_balance
            }

    return render_template(
        'generate_report.html',
        client=client,
        default_target=default_target,
        quarter_str=q_str,
        prev_balances=prev_balances,
        last_report=last_report
    )

@app.route('/report/<int:id>')
def report_view(id):
    report = db.session.get(Report, id)
    if not report:
        flash('Report not found.', 'error')
        return redirect(url_for('index'))

    # Calculate net worth aggregates
    retirement1_total = sum(bal.balance for bal in report.balances if bal.account.account_type == 'retirement_client1')
    retirement2_total = sum(bal.balance for bal in report.balances if bal.account.account_type == 'retirement_client2')
    non_retirement_total = sum(bal.balance for bal in report.balances if bal.account.account_type == 'non_retirement')
    trust_total = sum(bal.balance for bal in report.balances if bal.account.account_type == 'trust')
    grand_total_net_worth = retirement1_total + retirement2_total + non_retirement_total + trust_total
    
    liabilities = [bal for bal in report.balances if bal.account.is_liability]
    liabilities_total = sum(bal.balance for bal in liabilities)

    return render_template(
        'report.html',
        report=report,
        retirement1_total=retirement1_total,
        retirement2_total=retirement2_total,
        non_retirement_total=non_retirement_total,
        trust_total=trust_total,
        grand_total_net_worth=grand_total_net_worth,
        liabilities=liabilities,
        liabilities_total=liabilities_total
    )

@app.route('/report/<int:id>/pdf/sacs')
def report_pdf_sacs(id):
    report = db.session.get(Report, id)
    if not report:
        flash('Report not found.', 'error')
        return redirect(url_for('index'))
    pdf = generate_sacs_pdf(report)
    return send_file(pdf, mimetype='application/pdf', as_attachment=True, download_name=f'SACS_{report.client.name.replace(" ", "_")}_{report.quarter}.pdf')

@app.route('/report/<int:id>/pdf/tcc')
def report_pdf_tcc(id):
    report = db.session.get(Report, id)
    if not report:
        flash('Report not found.', 'error')
        return redirect(url_for('index'))
    pdf = generate_tcc_pdf(report)
    return send_file(pdf, mimetype='application/pdf', as_attachment=True, download_name=f'TCC_{report.client.name.replace(" ", "_")}_{report.quarter}.pdf')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
