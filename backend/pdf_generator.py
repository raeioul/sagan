import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing, Polygon, Line, Rect, Circle, String
from reportlab.pdfgen import canvas
import math

# Colors
BRAND_BLUE = colors.HexColor('#0f172a')
GREEN = colors.HexColor('#10b981')
GREEN_LIGHT = colors.HexColor('#d1fae5')
RED = colors.HexColor('#ef4444')
RED_LIGHT = colors.HexColor('#fee2e2')
BLUE = colors.HexColor('#3b82f6')
BLUE_LIGHT = colors.HexColor('#dbeafe')
FICA_COLOR = colors.HexColor('#0ea5e9')
FICA_LIGHT = colors.HexColor('#e0f2fe')
INVEST_COLOR = colors.HexColor('#1e3a8a')
INVEST_LIGHT = colors.HexColor('#dbeafe')
GOLD = colors.HexColor('#f59e0b')
GOLD_LIGHT = colors.HexColor('#fef3c7')
DARK_GRAY = colors.HexColor('#334155')
MED_GRAY = colors.HexColor('#64748b')
LIGHT_GRAY = colors.HexColor('#f1f5f9')

def draw_arrow(c, x1, y1, x2, y2, color=colors.HexColor('#64748b'), width=1.5, label=""):
    """Draws a line with an arrowhead pointing from (x1, y1) to (x2, y2)."""
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1, y1, x2, y2)
    
    # Arrow head math
    angle = math.atan2(y2 - y1, x2 - x1)
    head_len = 8
    hx1 = x2 - head_len * math.cos(angle - math.pi/6)
    hy1 = y2 - head_len * math.sin(angle - math.pi/6)
    hx2 = x2 - head_len * math.cos(angle + math.pi/6)
    hy2 = y2 - head_len * math.sin(angle + math.pi/6)
    
    c.setFillColor(color)
    c.setStrokeColor(color)
    p = c.beginPath()
    p.moveTo(x2, y2)
    p.lineTo(hx1, hy1)
    p.lineTo(hx2, hy2)
    p.close()
    c.drawPath(p, fill=1, stroke=1)

    if label:
        c.setFont('Helvetica-Bold', 7)
        c.setFillColor(DARK_GRAY)
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 + 5
        c.drawCentredString(mid_x, mid_y, label)

def draw_double_arrow(c, x1, y1, x2, y2, color=colors.HexColor('#3b82f6'), width=2, label=""):
    """Draws a bi-directional arrow between (x1, y1) and (x2, y2)."""
    c.setStrokeColor(color)
    c.setLineWidth(width)
    c.line(x1 + 10, y1, x2 - 10, y2)
    
    # Left arrowhead
    c.setFillColor(color)
    p1 = c.beginPath()
    p1.moveTo(x1, y1)
    p1.lineTo(x1 + 8, y1 + 5)
    p1.lineTo(x1 + 8, y1 - 5)
    p1.close()
    c.drawPath(p1, fill=1, stroke=1)
    
    # Right arrowhead
    p2 = c.beginPath()
    p2.moveTo(x2, y2)
    p2.lineTo(x2 - 8, y2 + 5)
    p2.lineTo(x2 - 8, y2 - 5)
    p2.close()
    c.drawPath(p2, fill=1, stroke=1)
    
    if label:
        c.setFont('Helvetica-Bold', 8)
        c.setFillColor(color)
        c.drawCentredString((x1 + x2)/2, (y1 + y2)/2 + 8, label)

def draw_header(c, title, subtitle, width, height):
    """Draws a premium header bar for the page."""
    c.setFillColor(BRAND_BLUE)
    c.rect(0, height - 85, width, 85, fill=1, stroke=0)
    
    c.setFillColor(colors.white)
    c.setFont('Helvetica-Bold', 18)
    c.drawString(40, height - 40, title)
    
    c.setFillColor(colors.HexColor('#94a3b8'))
    c.setFont('Helvetica', 11)
    c.drawString(40, height - 60, subtitle)
    
    # Firm branding watermark
    c.drawRightString(width - 40, height - 50, 'Windbrook Solutions')

def draw_footer(c, page_num, width):
    """Draws a bottom watermark/footer line."""
    c.setStrokeColor(colors.HexColor('#e2e8f0'))
    c.setLineWidth(0.5)
    c.line(40, 45, width - 40, 45)
    
    c.setFont('Helvetica', 8)
    c.setFillColor(MED_GRAY)
    c.drawString(40, 30, 'Sagan Client Report Portal — Private & Confidential')
    c.drawRightString(width - 40, 30, f'Page {page_num}')


def generate_sacs_pdf(report):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter
    client = report.client

    # ------------------ PAGE 1: CASHFLOW HUB DIAGRAM ------------------
    draw_header(c, 'SIMPLE AUTOMATED CASHFLOW SYSTEM (SACS)', f'Client Cashflow Visualization — {client.name} — {report.quarter}', width, height)
    
    # 1. Income Sources (Left side)
    y_start = 580
    c.setFont('Helvetica-Bold', 10)
    c.setFillColor(DARK_GRAY)
    c.drawString(40, y_start, 'INCOME SOURCES')
    
    # Client 1 bubble
    c.setFillColor(LIGHT_GRAY)
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(1)
    c.roundRect(40, y_start - 50, 110, 36, 6, fill=1, stroke=1)
    c.setFillColor(DARK_GRAY)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(48, y_start - 30, client.name[:16])
    c.setFont('Helvetica', 10)
    c.drawString(48, y_start - 44, f'${client.monthly_salary:,.0f}/mo')
    
    # Client 2 bubble (if spouse exists)
    if client.spouse_name:
        c.setFillColor(LIGHT_GRAY)
        c.roundRect(40, y_start - 100, 110, 36, 6, fill=1, stroke=1)
        c.setFillColor(DARK_GRAY)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(48, y_start - 80, client.spouse_name[:16])
        c.setFont('Helvetica', 10)
        c.drawString(48, y_start - 94, f'${client.spouse_monthly_salary:,.0f}/mo')
        
    # 2. Inflow Hub (Green Circle, Center-Left)
    cx_in, cy_in = 240, 520
    r_in = 55
    # Fill opacity using reportlab color
    c.setFillColor(colors.Color(16/255, 185/255, 129/255, 0.12))
    c.setStrokeColor(GREEN)
    c.setLineWidth(2.5)
    c.circle(cx_in, cy_in, r_in, fill=1, stroke=1)
    
    c.setFillColor(GREEN)
    c.setFont('Helvetica-Bold', 11)
    c.drawCentredString(cx_in, cy_in + 20, 'INFLOW HUB')
    c.setFont('Helvetica-Bold', 15)
    c.drawCentredString(cx_in, cy_in, f'${report.inflow_balance:,.0f}')
    c.setFont('Helvetica', 8)
    c.setFillColor(DARK_GRAY)
    c.drawCentredString(cx_in, cy_in - 18, 'Current Hub Inflow')
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(GREEN)
    c.drawCentredString(cx_in, cy_in - 30, 'Floor: $1,000')

    # Draw arrows from Income Sources to Inflow Hub
    if client.spouse_name:
        draw_arrow(c, 150, y_start - 32, cx_in - r_in + 4, cy_in + 12)
        draw_arrow(c, 150, y_start - 82, cx_in - r_in + 4, cy_in - 12)
    else:
        draw_arrow(c, 150, y_start - 32, cx_in - r_in + 2, cy_in)

    # 3. Outflow Hub (Red Circle, Center-Right)
    cx_out, cy_out = 440, 520
    r_out = 55
    c.setFillColor(colors.Color(239/255, 68/255, 68/255, 0.12))
    c.setStrokeColor(RED)
    c.setLineWidth(2.5)
    c.circle(cx_out, cy_out, r_out, fill=1, stroke=1)
    
    c.setFillColor(RED)
    c.setFont('Helvetica-Bold', 11)
    c.drawCentredString(cx_out, cy_out + 20, 'OUTFLOW HUB')
    c.setFont('Helvetica-Bold', 15)
    c.drawCentredString(cx_out, cy_out, f'${report.outflow_balance:,.0f}')
    c.setFont('Helvetica', 8)
    c.setFillColor(DARK_GRAY)
    c.drawCentredString(cx_out, cy_out - 18, 'Current Hub Outflow')
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(RED)
    c.drawCentredString(cx_out, cy_out - 30, 'Floor: $1,000')

    # Arrow from Inflow Hub to Outflow Hub (Auto Transfer)
    draw_arrow(c, cx_in + r_in, cy_in, cx_out - r_out, cy_out, color=RED, width=2, label=f"Auto Transfer on 28th: ${report.outflow_balance:,.0f}")

    # 4. Monthly Expenses Box (Below Outflow Hub)
    c.setFillColor(LIGHT_GRAY)
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(1)
    c.roundRect(cx_out - 60, cy_out - 160, 120, 45, 6, fill=1, stroke=1)
    c.setFillColor(DARK_GRAY)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(cx_out, cy_out - 130, 'MONTHLY EXPENSES "X"')
    c.setFont('Helvetica', 11)
    c.drawCentredString(cx_out, cy_out - 148, f'${report.outflow_balance:,.0f}/mo')
    
    # Arrow Outflow -> Expenses
    draw_arrow(c, cx_out, cy_out - r_out, cx_out, cy_out - 115, color=RED, width=1.5)

    # 5. Private Reserve Bubble (Blue Circle, Bottom-Center)
    cx_res, cy_res = 340, 360
    r_res = 55
    c.setFillColor(colors.Color(59/255, 130/255, 246/255, 0.12))
    c.setStrokeColor(BLUE)
    c.setLineWidth(2.5)
    c.circle(cx_res, cy_res, r_res, fill=1, stroke=1)
    
    c.setFillColor(BLUE)
    c.setFont('Helvetica-Bold', 11)
    c.drawCentredString(cx_res, cy_res + 20, 'PRIVATE RESERVE')
    c.setFont('Helvetica-Bold', 15)
    c.drawCentredString(cx_res, cy_res, f'${report.private_reserve_balance:,.0f}')
    c.setFont('Helvetica', 8)
    c.setFillColor(DARK_GRAY)
    c.drawCentredString(cx_res, cy_res - 18, '(Savings & Wealth)')
    c.setFont('Helvetica-Bold', 8)
    c.setFillColor(BLUE)
    c.drawCentredString(cx_res, cy_res - 30, f'Surplus: ${ (report.inflow_balance - report.outflow_balance):,.0f}/mo')

    # Arrow from Inflow Hub to Private Reserve
    # Starts at lower right of Inflow circle and points to Private Reserve
    draw_arrow(c, cx_in + r_in*0.5, cy_in - r_in*0.8, cx_res - r_res*0.5, cy_res + r_res*0.8, color=BLUE, width=2, label="Remaining Surplus")

    # Legend / Description Text box at bottom
    c.setFillColor(LIGHT_GRAY)
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(0.5)
    c.roundRect(40, 75, width - 80, 100, 8, fill=1, stroke=1)
    
    c.setFillColor(BRAND_BLUE)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(55, 155, 'SYSTEM LOGIC & TRANSFER RULES')
    
    c.setFont('Helvetica', 9)
    c.setFillColor(DARK_GRAY)
    bullets = [
        "Inflow Hub (Green): The primary clearing hub where salaries are deposited. Floor balance of $1,000 is maintained.",
        "Outflow Hub (Red): Secondary checking account used strictly for bills and lifestyle expenses. Floor balance of $1,000 is maintained.",
        "Automated Transfer: Executed monthly on the 28th. The Outflow amount total is pushed dynamically from Inflow checking to Outflow checking.",
        "Remaining Surplus: Any residual cash above the $1,000 Inflow floor sweeps automatically into the Private Reserve savings account."
    ]
    y_bullet = 138
    for b in bullets:
        c.drawString(55, y_bullet, '• ' + b)
        y_bullet -= 15

    draw_footer(c, 1, width)
    c.showPage()

    # ------------------ PAGE 2: MAGNIFIED PRIVATE RESERVE ------------------
    draw_header(c, 'SACS LONG TERM CASHFLOW', f'Magnified Private Reserve Allocation — {client.name} — {report.quarter}', width, height)

    c.setFont('Helvetica-Bold', 12)
    c.setFillColor(BRAND_BLUE)
    c.drawString(40, height - 120, 'Under the Hood of the Private Reserve Circle')
    
    c.setFont('Helvetica', 10)
    c.setFillColor(DARK_GRAY)
    c.drawString(40, height - 138, 'Long-term surplus capital is allocated dynamically between immediate protection (FICA) and wealth growth (Investment).')

    # Draw FICA Account Box (Left Side)
    bx_fica, by_fica, bw, bh = 60, 400, 210, 140
    c.setFillColor(FICA_LIGHT)
    c.setStrokeColor(FICA_COLOR)
    c.setLineWidth(2)
    c.roundRect(bx_fica, by_fica, bw, bh, 8, fill=1, stroke=1)
    
    c.setFillColor(FICA_COLOR)
    c.setFont('Helvetica-Bold', 13)
    c.drawString(bx_fica + 15, by_fica + bh - 25, 'FICA ACCOUNT')
    c.setFont('Helvetica-Bold', 16)
    c.drawString(bx_fica + 15, by_fica + bh - 55, f'${report.private_reserve_balance:,.0f}')
    
    c.setFont('Helvetica', 9)
    c.setFillColor(DARK_GRAY)
    c.drawString(bx_fica + 15, by_fica + bh - 85, 'Safety Net Cap: 6X Expenses + Deductibles')
    c.setFont('Helvetica-Bold', 9)
    c.drawString(bx_fica + 15, by_fica + bh - 100, f'Target Safety Cap: ${report.target_amount:,.0f}')
    
    # Funding status
    c.setFont('Helvetica-Bold', 9)
    if report.private_reserve_balance >= report.target_amount:
        c.setFillColor(GREEN)
        c.drawString(bx_fica + 15, by_fica + 20, '✅ FULLY FUNDED (100%+)')
    else:
        funding_pct = (report.private_reserve_balance / report.target_amount) * 100 if report.target_amount else 0
        c.setFillColor(GOLD)
        c.drawString(bx_fica + 15, by_fica + 20, f'⚠️ FUNDING: {funding_pct:.0f}% OF CAP')

    # Draw Investment Account Box (Right Side)
    bx_inv, by_inv = 340, 400
    c.setFillColor(INVEST_LIGHT)
    c.setStrokeColor(INVEST_COLOR)
    c.setLineWidth(2)
    c.roundRect(bx_inv, by_inv, bw, bh, 8, fill=1, stroke=1)
    
    c.setFillColor(INVEST_COLOR)
    c.setFont('Helvetica-Bold', 13)
    c.drawString(bx_inv + 15, by_inv + bh - 25, 'INVESTMENT ACCOUNT')
    c.setFont('Helvetica-Bold', 16)
    c.drawString(bx_inv + 15, by_inv + bh - 55, f'${report.schwab_brokerage_balance:,.0f}')
    
    c.setFont('Helvetica', 9)
    c.setFillColor(DARK_GRAY)
    c.drawString(bx_inv + 15, by_inv + bh - 85, 'Generates long-term wealth growth.')
    c.drawString(bx_inv + 15, by_inv + bh - 100, 'Funds sweep here once FICA is filled.')
    
    c.setFont('Helvetica-Bold', 9)
    c.setFillColor(INVEST_COLOR)
    c.drawString(bx_inv + 15, by_inv + 20, '📈 ASSET ACCUMULATION TYPE')

    # Dynamic Arrow between accounts representing automated rebalancing
    draw_double_arrow(c, bx_fica + bw, by_fica + bh/2, bx_inv, by_inv + bh/2, label="Automated Rebalancing")

    # Math calculations box
    y_calc = 150
    c.setFillColor(LIGHT_GRAY)
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(0.5)
    c.roundRect(40, y_calc, width - 80, 200, 8, fill=1, stroke=1)
    
    c.setFillColor(BRAND_BLUE)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(55, y_calc + 175, 'TARGET CAP CALCULATION DETAIL')
    
    # Display the math breakdown
    c.setFont('Helvetica', 10)
    c.setFillColor(DARK_GRAY)
    c.drawString(55, y_calc + 145, 'Formula: (6 × Monthly Expenses) + All Insurance Policy Deductibles')
    c.line(55, y_calc + 137, width - 55, y_calc + 137)
    
    # 6x normal expenses
    ex_6 = 6 * report.outflow_balance
    c.drawString(60, y_calc + 115, f'• 6 Months Normal Expenses:  6 × ${report.outflow_balance:,.0f}')
    c.drawRightString(width - 60, y_calc + 115, f'${ex_6:,.2f}')
    
    # Insurance policy deductibles
    total_ded = sum(d.amount for d in client.deductibles)
    c.drawString(60, y_calc + 95, f'• Insurance Policy Deductibles:  Sum of {len(client.deductibles)} policy items')
    c.drawRightString(width - 60, y_calc + 95, f'+ ${total_ded:,.2f}')
    
    # Deductible itemization text
    ded_text = ", ".join(f"{d.label} (${d.amount:,.0f})" for d in client.deductibles)
    c.setFont('Helvetica-Oblique', 8)
    c.setFillColor(MED_GRAY)
    c.drawString(70, y_calc + 80, f"({ded_text})" if ded_text else "(No specific policy deductibles configured - default target sum applied)")
    
    # Total safety cap target
    c.setFont('Helvetica-Bold', 10)
    c.setFillColor(BRAND_BLUE)
    c.drawString(60, y_calc + 55, 'TOTAL CALCULATED SAFETY TARGET CAP')
    c.drawRightString(width - 60, y_calc + 55, f'${report.target_amount:,.2f}')
    
    # Current Funding Surplus/Deficit
    c.setFont('Helvetica-Bold', 10)
    surplus_def = report.private_reserve_balance - report.target_amount
    if surplus_def >= 0:
        c.setFillColor(GREEN)
        c.drawString(60, y_calc + 30, 'FICA Funding Surplus (Ready for Investment Sweep)')
        c.drawRightString(width - 60, y_calc + 30, f'${surplus_def:,.2f}')
    else:
        c.setFillColor(RED)
        c.drawString(60, y_calc + 30, 'FICA Funding Deficit (Sweeps temporarily restricted)')
        c.drawRightString(width - 60, y_calc + 30, f'${abs(surplus_def):,.2f}')

    draw_footer(c, 2, width)
    c.save()
    buf.seek(0)
    return buf


def generate_tcc_pdf(report):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter
    client = report.client

    draw_header(c, 'TOTAL CLIENT CHART (TCC)', f'Consolidated Net Worth Map — {client.name} — {report.quarter}', width, height)

    # 1. Green Client Info Badges
    y_info = height - 120
    c.setFillColor(GREEN_LIGHT)
    c.setStrokeColor(GREEN)
    c.setLineWidth(1)
    
    # Client 1 Badge
    c.roundRect(40, y_info - 45, 250, 42, 6, fill=1, stroke=1)
    c.setFillColor(colors.HexColor('#065f46'))
    c.setFont('Helvetica-Bold', 10)
    c.drawString(50, y_info - 18, client.name)
    c.setFont('Helvetica', 9)
    c.drawString(50, y_info - 36, f'DOB: {client.dob.strftime("%m/%d/%Y")} ({client.age} yrs) | SSN: ***-**-{client.last_four_ssn}')

    # Client 2 Badge
    if client.spouse_name:
        c.setFillColor(GREEN_LIGHT)
        c.setStrokeColor(GREEN)
        c.roundRect(320, y_info - 45, 250, 42, 6, fill=1, stroke=1)
        c.setFillColor(colors.HexColor('#065f46'))
        c.setFont('Helvetica-Bold', 10)
        c.drawString(330, y_info - 18, client.spouse_name)
        c.setFont('Helvetica', 9)
        c.drawString(330, y_info - 36, f'DOB: {client.spouse_dob.strftime("%m/%d/%Y")} ({client.spouse_age} yrs) | SSN: ***-**-{client.spouse_last_four_ssn}')

    # Set up Asset Structure Sections dynamically
    # Category totals
    ret1_bal = sum(b.balance for b in report.balances if b.account.account_type == 'retirement_client1')
    ret2_bal = sum(b.balance for b in report.balances if b.account.account_type == 'retirement_client2')
    non_ret_bal = sum(b.balance for b in report.balances if b.account.account_type == 'non_retirement')
    trust_bal = sum(b.balance for b in report.balances if b.account.account_type == 'trust')
    net_worth_total = ret1_bal + ret2_bal + non_ret_bal + trust_bal
    
    liabilities = [b for b in report.balances if b.account.is_liability]
    liabilities_total = sum(b.balance for b in liabilities)

    # Asset Grid Columns: left=Client 1 assets, right=Client 2/Joint assets
    # Draw Asset Cards
    y_assets = height - 195
    card_h = 190
    card_w = 250
    
    # Card 1: Retirement Accounts (Top-Left Client 1, Top-Right Client 2)
    c.setFillColor(BLUE_LIGHT)
    c.setStrokeColor(BLUE)
    c.setLineWidth(1)
    c.roundRect(40, y_assets - card_h, card_w, card_h, 8, fill=1, stroke=1)
    
    c.setFillColor(BLUE)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(55, y_assets - 25, f"{client.name.split()[0]}'s Retirement Assets")
    
    # Loop assets Client 1
    y_item = y_assets - 45
    c.setFont('Helvetica', 8.5)
    c.setFillColor(DARK_GRAY)
    c1_ret_list = [b for b in report.balances if b.account.account_type == 'retirement_client1']
    for b in c1_ret_list[:5]: # Cap at 5 display bubbles inside the card
        acc = b.account
        lbl = f"{acc.name[:16]} (*{acc.last_four or ''})"
        c.drawString(55, y_item, lbl)
        
        val_str = f"${b.balance:,.0f}"
        if b.cash_balance is not None:
            val_str += f" (Cash: ${b.cash_balance:,.0f})"
        c.drawRightString(40 + card_w - 15, y_item, val_str)
        y_item -= 18

    # Retirement 1 Total display
    c.setFont('Helvetica-Bold', 10)
    c.setFillColor(BLUE)
    c.drawString(55, y_assets - card_h + 15, 'Total Client 1 Retirement')
    c.drawRightString(40 + card_w - 15, y_assets - card_h + 15, f'${ret1_bal:,.0f}')

    # Right Card: Client 2 Retirement (or Non-Retirement if single client)
    c.setFillColor(BLUE_LIGHT)
    c.setStrokeColor(BLUE)
    c.roundRect(320, y_assets - card_h, card_w, card_h, 8, fill=1, stroke=1)
    
    c.setFillColor(BLUE)
    c.setFont('Helvetica-Bold', 11)
    if client.spouse_name:
        c.drawString(335, y_assets - 25, f"{client.spouse_name.split()[0]}'s Retirement Assets")
        y_item = y_assets - 45
        c.setFont('Helvetica', 8.5)
        c.setFillColor(DARK_GRAY)
        c2_ret_list = [b for b in report.balances if b.account.account_type == 'retirement_client2']
        for b in c2_ret_list[:5]:
            acc = b.account
            lbl = f"{acc.name[:16]} (*{acc.last_four or ''})"
            c.drawString(335, y_item, lbl)
            val_str = f"${b.balance:,.0f}"
            if b.cash_balance is not None:
                val_str += f" (Cash: ${b.cash_balance:,.0f})"
            c.drawRightString(320 + card_w - 15, y_item, val_str)
            y_item -= 18
            
        c.setFont('Helvetica-Bold', 10)
        c.setFillColor(BLUE)
        c.drawString(335, y_assets - card_h + 15, 'Total Client 2 Retirement')
        c.drawRightString(320 + card_w - 15, y_assets - card_h + 15, f'${ret2_bal:,.0f}')
    else:
        # If single client, draw a placeholder or helpful wealth planning rule
        c.drawString(335, y_assets - 25, "Financial Safety Caps")
        c.setFont('Helvetica', 9)
        c.setFillColor(DARK_GRAY)
        c.drawString(335, y_assets - 55, "FICA target safety reserve acts as the")
        c.drawString(335, y_assets - 70, "essential household defense layer.")
        c.drawString(335, y_assets - 95, "Once safety goals are met, assets")
        c.drawString(335, y_assets - 110, "cascade continuously into long term")
        c.drawString(335, y_assets - 125, "Schawb wealth growth accounts.")

    # Card 3: Non-Retirement Joint Accounts (Bottom-Left)
    y_assets2 = y_assets - card_h - 20
    c.setFillColor(GOLD_LIGHT)
    c.setStrokeColor(GOLD)
    c.roundRect(40, y_assets2 - card_h, card_w, card_h, 8, fill=1, stroke=1)
    
    c.setFillColor(colors.HexColor('#9a3412'))
    c.setFont('Helvetica-Bold', 11)
    c.drawString(55, y_assets2 - 25, 'Non-Retirement Accounts')
    
    y_item = y_assets2 - 45
    c.setFont('Helvetica', 8.5)
    c.setFillColor(DARK_GRAY)
    non_ret_list = [b for b in report.balances if b.account.account_type == 'non_retirement']
    for b in non_ret_list[:5]:
        acc = b.account
        lbl = f"{acc.name[:16]} (*{acc.last_four or ''})"
        c.drawString(55, y_item, lbl)
        val_str = f"${b.balance:,.0f}"
        if b.cash_balance is not None:
            val_str += f" (Cash: ${b.cash_balance:,.0f})"
        c.drawRightString(40 + card_w - 15, y_item, val_str)
        y_item -= 18
        
    c.setFont('Helvetica-Bold', 10)
    c.setFillColor(colors.HexColor('#9a3412'))
    c.drawString(55, y_assets2 - card_h + 15, 'Total Non-Retirement')
    c.drawRightString(40 + card_w - 15, y_assets2 - card_h + 15, f'${non_ret_bal:,.0f}')

    # Card 4: Trust & Real Estate Assets (Bottom-Right)
    c.setFillColor(GOLD_LIGHT)
    c.setStrokeColor(GOLD)
    c.roundRect(320, y_assets2 - card_h, card_w, card_h, 8, fill=1, stroke=1)
    
    c.setFillColor(colors.HexColor('#9a3412'))
    c.setFont('Helvetica-Bold', 11)
    c.drawString(335, y_assets2 - 25, 'Trust & Property Assets')
    
    y_item = y_assets2 - 45
    c.setFont('Helvetica', 8.5)
    c.setFillColor(DARK_GRAY)
    trust_list = [b for b in report.balances if b.account.account_type == 'trust']
    for b in trust_list[:5]:
        acc = b.account
        lbl = f"{acc.name[:16]}"
        c.drawString(335, y_item, lbl)
        if acc.property_address:
            c.setFont('Helvetica-Oblique', 7.5)
            c.setFillColor(MED_GRAY)
            c.drawString(335, y_item - 12, acc.property_address[:40])
            c.setFont('Helvetica', 8.5)
            c.setFillColor(DARK_GRAY)
            y_item -= 12
        c.drawRightString(320 + card_w - 15, y_item, f"${b.balance:,.0f}")
        y_item -= 18
        
    c.setFont('Helvetica-Bold', 10)
    c.setFillColor(colors.HexColor('#9a3412'))
    c.drawString(335, y_assets2 - card_h + 15, 'Total Trust / Properties')
    c.drawRightString(320 + card_w - 15, y_assets2 - card_h + 15, f'${trust_bal:,.0f}')

    # Card 5: Grand Net Worth Summary Box (Middle Center Overlaid or below)
    y_net = y_assets2 - card_h - 25
    c.setFillColor(colors.HexColor('#f8fafc'))
    c.setStrokeColor(BRAND_BLUE)
    c.setLineWidth(1.5)
    c.roundRect(40, y_net - 45, width - 80, 40, 6, fill=1, stroke=1)
    
    c.setFillColor(BRAND_BLUE)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(55, y_net - 28, 'GRAND TOTAL ASSETS (NET WORTH)')
    c.drawRightString(width - 55, y_net - 28, f'${net_worth_total:,.0f}')

    # Card 6: Liabilities Tracker (Separate Table Box, bottom)
    y_liab = y_net - 60
    c.setFillColor(BRAND_BLUE)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(40, y_liab, 'LIABILITIES & DEBTS (TRACKED SEPARATELY)')
    c.line(40, y_liab - 5, width - 40, y_liab - 5)

    if liabilities:
        # Render a simple ReportLab Table
        data = [['Debt Category / Account Name', 'Interest Rate', 'Remaining Balance']]
        for bal in liabilities:
            rate = f"{bal.account.interest_rate:.1f}%" if bal.account.interest_rate is not None else '—'
            data.append([bal.account.name, rate, f"${bal.balance:,.0f}"])
        data.append(['TOTAL LIABILITIES', '', f"${liabilities_total:,.0f}"])
        
        # Draw table
        col_widths = [260, 110, 162]
        table = Table(data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), BRAND_BLUE),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, LIGHT_GRAY]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#fee2e2')),
            ('TEXTCOLOR', (0, -1), (-1, -1), RED),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        table.wrapOn(c, width, height)
        # Calculate table height: len(data) * row_height
        table_h = len(data) * 18
        table.drawOn(c, 40, y_liab - table_h - 15)
    else:
        c.setFont('Helvetica-Oblique', 10)
        c.setFillColor(MED_GRAY)
        c.drawString(45, y_liab - 25, 'No liabilities configured for this client.')

    draw_footer(c, 1, width)
    c.save()
    buf.seek(0)
    return buf
