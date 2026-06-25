/* Sagan Cashflow Portal Interaction Logic - app.js */

document.addEventListener('DOMContentLoaded', function () {
    
    // 1. SACS Real-time Surplus Calculator
    const inflowInput = document.getElementById('inflow_balance');
    const outflowInput = document.getElementById('outflow_balance');
    const excessOutput = document.getElementById('sacs-excess');

    function calculateSurplus() {
        const inflowVal = parseFloat(inflowInput.value) || 0;
        const outflowVal = parseFloat(outflowInput.value) || 0;
        const surplus = inflowVal - outflowVal;
        
        if (excessOutput) {
            excessOutput.value = '$' + surplus.toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        }
    }

    if (inflowInput && outflowInput) {
        inflowInput.addEventListener('input', calculateSurplus);
        outflowInput.addEventListener('input', calculateSurplus);
        calculateSurplus(); // Run initially
    }

    // 2. Pre-Meeting Checklist Dynamic Interactions
    const checklistCheckboxes = document.querySelectorAll('.checklist-checkbox');
    checklistCheckboxes.forEach(chk => {
        // Load saved state from localStorage if wanted
        const savedState = localStorage.getItem(chk.id);
        if (savedState === 'checked') {
            chk.checked = true;
            chk.closest('.checklist-item').classList.add('checked');
        }

        chk.addEventListener('change', function () {
            if (this.checked) {
                this.closest('.checklist-item').classList.add('checked');
                localStorage.setItem(this.id, 'checked');
            } else {
                this.closest('.checklist-item').classList.remove('checked');
                localStorage.removeItem(this.id);
            }
        });
    });

    // 3. Pre-fill "Use Last Value" Helper Buttons
    const useLastButtons = document.querySelectorAll('.btn-use-last');
    useLastButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const targetId = this.getAttribute('data-target');
            const value = this.getAttribute('data-value');
            const inputField = document.getElementById(targetId);
            if (inputField) {
                inputField.value = value;
                // Trigger input event to update any active calculations
                inputField.dispatchEvent(new Event('input'));
            }
        });
    });

    // 4. Client Profile Editor: Add/Remove Insurance Deductibles dynamically
    const addDeductibleBtn = document.getElementById('btn-add-deductible');
    const deductiblesContainer = document.getElementById('deductibles-container');

    if (addDeductibleBtn && deductiblesContainer) {
        addDeductibleBtn.addEventListener('click', function () {
            const rows = deductiblesContainer.querySelectorAll('.deductible-row');
            let clone = null;
            
            if (rows.length > 0) {
                clone = rows[0].cloneNode(true);
            } else {
                // Fallback if container is empty
                const newRow = document.createElement('div');
                newRow.className = 'deductible-row form-row';
                newRow.innerHTML = `
                    <input type="hidden" name="deductible_id[]" value="">
                    <div class="col-field"><input type="text" name="deductible_label[]" placeholder="e.g. Health Insurance"></div>
                    <div class="col-field"><input type="number" name="deductible_amount[]" step="0.01" min="0" placeholder="Amount ($)"></div>
                    <button type="button" class="btn btn-danger btn-sm remove-row-btn">&times;</button>
                `;
                clone = newRow;
            }

            // Reset clone inputs
            clone.querySelector('input[type="hidden"]').value = "";
            clone.querySelectorAll('input[type="text"], input[type="number"]').forEach(input => input.value = "");
            
            // Setup remove button
            const removeBtn = clone.querySelector('.remove-row-btn');
            removeBtn.style.display = 'flex';
            removeBtn.addEventListener('click', function () {
                clone.remove();
            });

            deductiblesContainer.appendChild(clone);
        });

        // Setup click listeners for any pre-rendered remove buttons
        deductiblesContainer.querySelectorAll('.deductible-row').forEach(row => {
            const removeBtn = row.querySelector('.remove-row-btn');
            if (removeBtn) {
                removeBtn.addEventListener('click', function () {
                    // Only remove if it's not the last remaining row, or allow it but keep track
                    if (deductiblesContainer.querySelectorAll('.deductible-row').length > 1) {
                        row.remove();
                    } else {
                        // Clear values instead of removing the last template row
                        row.querySelector('input[type="hidden"]').value = "";
                        row.querySelectorAll('input[type="text"], input[type="number"]').forEach(input => input.value = "");
                    }
                });
            }
        });
    }

    // 5. Client Profile Editor: Add/Remove Account Configurations dynamically
    const addAccountBtn = document.getElementById('btn-add-account');
    const accountsContainer = document.getElementById('accounts-container');

    if (addAccountBtn && accountsContainer) {
        addAccountBtn.addEventListener('click', function () {
            const rows = accountsContainer.querySelectorAll('.account-row');
            let clone = null;

            if (rows.length > 0) {
                clone = rows[0].cloneNode(true);
            } else {
                // Fallback template
                const newRow = document.createElement('div');
                newRow.className = 'account-row form-row';
                newRow.innerHTML = `
                    <input type="hidden" name="account_id[]" value="">
                    <div class="col-field"><input type="text" name="account_name[]" placeholder="e.g. Schwab IRA" required></div>
                    <div class="col-field">
                        <select name="account_type[]" onchange="togglePropertyAddress(this)" required>
                            <option value="non_retirement">Non-Retirement</option>
                            <option value="retirement_client1">Retirement (Client 1)</option>
                            <option value="retirement_client2">Retirement (Client 2)</option>
                            <option value="trust">Trust Asset / Property</option>
                            <option value="liability">Liability / Debt</option>
                        </select>
                    </div>
                    <div class="col-field">
                        <select name="account_owner[]" required>
                            <option value="joint">Joint</option>
                            <option value="client1">Client 1</option>
                            <option value="client2">Client 2</option>
                            <option value="trust">Trust</option>
                        </select>
                    </div>
                    <div class="col-field"><input type="text" name="account_last_four[]" maxlength="4" pattern="\\d{4}" placeholder="e.g. 1234"></div>
                    <div class="col-field"><input type="number" name="account_interest_rate[]" step="0.01" min="0" placeholder="—"></div>
                    <div class="col-field prop-addr-col"><input type="text" name="account_property_address[]" placeholder="123 Main St, Atlanta, GA" class="prop-addr-input" style="display:none"></div>
                    <button type="button" class="btn btn-danger btn-sm remove-row-btn">&times;</button>
                `;
                clone = newRow;
            }

            // Reset fields
            clone.querySelector('input[type="hidden"]').value = "";
            clone.querySelectorAll('input[type="text"], input[type="number"]').forEach(input => input.value = "");
            clone.querySelectorAll('select').forEach(select => select.selectedIndex = 0);

            // Enable delete button on the clone
            const removeBtn = clone.querySelector('.remove-row-btn');
            removeBtn.style.display = 'flex';
            removeBtn.addEventListener('click', function () {
                clone.remove();
            });

            accountsContainer.appendChild(clone);
        });

        // Setup removal on existing accounts
        accountsContainer.querySelectorAll('.account-row').forEach(row => {
            const removeBtn = row.querySelector('.remove-row-btn');
            if (removeBtn) {
                removeBtn.addEventListener('click', function () {
                    if (accountsContainer.querySelectorAll('.account-row').length > 1) {
                        row.remove();
                    } else {
                        // Clear last row instead of deleting structure entirely
                        row.querySelector('input[type="hidden"]').value = "";
                        row.querySelectorAll('input[type="text"], input[type="number"]').forEach(input => input.value = "");
                        row.querySelectorAll('select').forEach(select => select.selectedIndex = 0);
                    }
                });
            }
        });
    }

    // 6. MaxLength limiting on digits pattern inputs
    document.querySelectorAll('input[pattern]').forEach(input => {
        input.addEventListener('input', function () {
            const max = parseInt(this.getAttribute('maxlength'));
            if (max && this.value.length > max) {
                this.value = this.value.slice(0, max);
            }
        });
    });

    // 7. Highlight incomplete required fields
    function updateIncompleteFields() {
        const requiredInputs = document.querySelectorAll('.balance-input[required]');
        requiredInputs.forEach(input => {
            const val = input.value.trim();
            const row = input.closest('.account-entry-row');
            if (!row) return;
            if (val === '') {
                row.classList.add('incomplete');
            } else {
                row.classList.remove('incomplete');
            }
        });
    }

    document.querySelectorAll('.balance-input').forEach(input => {
        input.addEventListener('input', updateIncompleteFields);
    });
    updateIncompleteFields();

    // 8. Toggle property address field visibility based on account type
    window.togglePropertyAddress = function(selectEl) {
        const row = selectEl.closest('.account-row');
        if (!row) return;
        const addrInput = row.querySelector('.prop-addr-input');
        if (!addrInput) return;
        addrInput.style.display = selectEl.value === 'trust' ? 'block' : 'none';
    };

    // Run on page load for existing rows
    document.querySelectorAll('.account-row select[name="account_type[]"]').forEach(sel => {
        window.togglePropertyAddress(sel);
    });

    // 9. Real-time TCC Totals Calculation
    function calculateTCCTotals() {
        const balanceInputs = document.querySelectorAll('.balance-input');
        let ret1 = 0, ret2 = 0, nonret = 0, trust = 0, liab = 0;

        balanceInputs.forEach(input => {
            const val = parseFloat(input.value) || 0;
            const accType = input.getAttribute('data-acc-type');
            const isLiab = input.getAttribute('data-is-liability') === 'true';

            if (isLiab) {
                liab += val;
            } else if (accType === 'retirement_client1') {
                ret1 += val;
            } else if (accType === 'retirement_client2') {
                ret2 += val;
            } else if (accType === 'non_retirement') {
                nonret += val;
            } else if (accType === 'trust') {
                trust += val;
            }
        });

        const grand = ret1 + ret2 + nonret + trust;

        const fmt = (v) => '$' + v.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 });

        const setVal = (id, v) => {
            const el = document.getElementById(id);
            if (el) el.textContent = fmt(v);
        };

        setVal('total-ret1', ret1);
        setVal('total-ret2', ret2);
        setVal('total-nonret', nonret);
        setVal('total-trust', trust);
        setVal('total-grand', grand);
        setVal('total-liab', liab);
    }

    // Attach event listeners to all balance inputs
    document.querySelectorAll('.balance-input').forEach(input => {
        input.addEventListener('input', calculateTCCTotals);
    });

    // Run initial calculation
    calculateTCCTotals();
});
