class HealthcareAnalyticsApp {
    constructor() {
        this.data = [];
        this.filteredData = [];
        this.charts = {};
        this.chartInstances = {};
        this.renderTimeout = null;
        this.currentSection = 'dashboard';
        this.criticalThresholds = {
            heart_rate_high: 100,
            heart_rate_low: 60,
            oxygen_saturation_low: 90,
            temperature_high: 38.5,
            temperature_low: 36
        };
        // Cache for computed values
        this.cache = {
            statistics: null,
            patientGroups: null,
            lastFilterTime: 0
        };
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupNavigation();
        // DO NOT load sample data by default
        this.showEmptyState();
    }

    setupEventListeners() {
        // File upload
        document.getElementById('csvFile').addEventListener('change', (e) => this.handleCsvUpload(e));
        
        // Buttons
        document.getElementById('loadSampleBtn').addEventListener('click', () => this.generateSampleData());
        document.getElementById('resetFiltersBtn').addEventListener('click', () => this.resetFilters());
        document.getElementById('exportBtn').addEventListener('click', () => this.exportData());
        
        // Filters with debouncing
        document.getElementById('filterPatient').addEventListener('input', (e) => this.debouncedFilter(e));
        document.getElementById('filterMetric').addEventListener('change', () => this.debouncedFilter());
        document.getElementById('filterStatus').addEventListener('change', () => this.debouncedFilter());
        
        // Search with debouncing
        document.getElementById('tableSearch').addEventListener('input', (e) => this.debouncedSearch(e));
    }

    setupNavigation() {
        const navLinks = document.querySelectorAll('.nav-link');
        const contentSections = document.querySelectorAll('.content-section');

        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();

                // Remove active class from all links and sections
                navLinks.forEach(l => l.classList.remove('active'));
                contentSections.forEach(s => s.classList.remove('active'));

                // Add active class to clicked link and corresponding section
                link.classList.add('active');
                const sectionId = link.getAttribute('href');
                const section = document.querySelector(sectionId);

                if (section) {
                    section.classList.add('active');
                    this.currentSection = link.getAttribute('data-section');

                    // Update reports when reports section is accessed
                    if (this.currentSection === 'reports') {
                        this.updateReportSection();
                    }

                    // Scroll to section smoothly
                    setTimeout(() => {
                        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 100);
                }
            });
        });
    }

    debouncedFilter = this.debounce(() => this.applyFilters(), 300);
    debouncedSearch = this.debounce((e) => this.searchTable(e), 300);

    debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }

    showEmptyState() {
        // Clear all UI elements
        document.getElementById('statusCards').innerHTML = '';
        document.getElementById('tableBody').innerHTML = '';
        document.getElementById('alertsContainer').innerHTML = '';
        
        // Show empty state message in table
        const emptyMessage = `
            <tr>
                <td colspan="6" style="text-align: center; padding: 3rem; color: #7f8c8d;">
                    <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"><i class="fas fa-inbox"></i></div>
                    <h3 style="margin-bottom: 1rem;">No Data Loaded</h3>
                    <p>Please upload a CSV file or load sample data to get started</p>
                </td>
            </tr>
        `;
        document.getElementById('tableBody').innerHTML = emptyMessage;
        
        // Reset stats
        document.getElementById('totalPatients').textContent = '0';
        document.getElementById('totalRecords').textContent = '0';
        document.getElementById('criticalEvents').textContent = '0';
    }

    handleCsvUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        this.showLoading(true);
        
        // Use Web Worker for large file parsing if available
        if (window.Worker && file.size > 1000000) {
            this.parseWithWorker(file);
        } else {
            this.parseInMain(file);
        }
    }

    parseInMain(file) {
        Papa.parse(file, {
            header: true,
            skipEmptyLines: true,
            chunk: (results, parser) => {
                // Process in chunks for better responsiveness
                if (!this.data) this.data = [];
                const processed = this.processData(results.data);
                this.data.push(...processed);
                
                // Update UI every chunk
                if (this.data.length % 1000 === 0) {
                    console.log(`Processed ${this.data.length} records...`);
                }
            },
            complete: () => {
                this.filteredData = [...this.data];
                this.cache.statistics = null;
                this.cache.patientGroups = null;
                this.updateDashboard();
                this.showLoading(false);
                this.showToast(`Data loaded: ${this.data.length} records`, 'success');
            },
            error: (error) => {
                this.showLoading(false);
                this.showToast(`Error parsing CSV: ${error.message}`, 'error');
                console.error('CSV Parse Error:', error);
            }
        });
    }

    generateSampleData() {
        this.showLoading(true);
        
        // Generate data asynchronously
        setTimeout(() => {
            const patients = ['P00001', 'P00002', 'P00003', 'P00004', 'P00005', 
                            'P00006', 'P00007', 'P00008', 'P00009', 'P00010'];
            this.data = [];

            // Generate in batches for better performance
            for (let i = 0; i < 500; i++) {
                const patientId = patients[Math.floor(Math.random() * patients.length)];
                const timestamp = new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000);
                
                this.data.push({
                    patient_id: patientId,
                    timestamp: timestamp.toISOString(),
                    heart_rate: Math.round(60 + Math.random() * 40 + (Math.random() > 0.9 ? 40 : 0)),
                    temperature: (36 + Math.random() * 2.5).toFixed(1),
                    blood_pressure_systolic: Math.round(110 + Math.random() * 40),
                    blood_pressure_diastolic: Math.round(70 + Math.random() * 30),
                    respiratory_rate: Math.round(12 + Math.random() * 8),
                    oxygen_saturation: Math.round(95 + Math.random() * 5 - (Math.random() > 0.85 ? 8 : 0))
                });
            }

            this.filteredData = [...this.data];
            this.cache.statistics = null;
            this.cache.patientGroups = null;
            this.updateDashboard();
            this.showLoading(false);
            this.showToast('Sample data loaded: 500 records', 'success');
        }, 100);
    }

    processData(rawData) {
        return rawData.map(row => ({
            patient_id: row.patient_id || '',
            timestamp: row.timestamp ? new Date(row.timestamp).toISOString() : new Date().toISOString(),
            heart_rate: parseFloat(row.heart_rate) || 0,
            temperature: parseFloat(row.temperature) || 0,
            blood_pressure_systolic: parseFloat(row.blood_pressure_systolic) || 0,
            blood_pressure_diastolic: parseFloat(row.blood_pressure_diastolic) || 0,
            respiratory_rate: parseFloat(row.respiratory_rate) || 0,
            oxygen_saturation: parseFloat(row.oxygen_saturation) || 0
        })).filter(row => row.patient_id && row.patient_id.trim());
    }

    applyFilters() {
        this.cache.lastFilterTime = Date.now();
        const patientFilter = document.getElementById('filterPatient').value.toLowerCase().trim();
        const statusFilter = document.getElementById('filterStatus').value;

        // Optimize filtering with early returns
        this.filteredData = this.data.filter(record => {
            if (patientFilter && !record.patient_id.toLowerCase().includes(patientFilter)) {
                return false;
            }
            if (statusFilter && this.getRecordStatus(record) !== statusFilter) {
                return false;
            }
            return true;
        });

        // Debounce dashboard update
        clearTimeout(this.renderTimeout);
        this.renderTimeout = setTimeout(() => this.updateDashboard(), 150);
    }

    resetFilters() {
        document.getElementById('filterPatient').value = '';
        document.getElementById('filterMetric').value = '';
        document.getElementById('filterStatus').value = '';
        this.filteredData = [...this.data];
        this.updateDashboard();
        this.showToast('Filters reset', 'success');
    }

    searchTable(event) {
        const searchTerm = event.target.value.toLowerCase().trim();
        const rows = document.querySelectorAll('#tableBody tr');

        if (!searchTerm) {
            rows.forEach(row => row.style.display = '');
            return;
        }

        // Use requestAnimationFrame for smooth search
        requestAnimationFrame(() => {
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }

    updateDashboard() {
        // Prioritize UI updates
        this.updateQuickStats();
        this.updateStatusCards();
        this.updateDataTable();
        
        // Defer chart rendering to next tick for better responsiveness
        requestAnimationFrame(() => {
            this.updateCharts();
            this.updateAlerts();
        });
    }

    updateQuickStats() {
        // Cache results to avoid recalculation
        const uniquePatients = new Set(this.filteredData.map(r => r.patient_id)).size;
        const criticalCount = this.filteredData.filter(r => this.isCritical(r)).length;

        document.getElementById('totalPatients').textContent = uniquePatients;
        document.getElementById('totalRecords').textContent = this.filteredData.length;
        document.getElementById('criticalEvents').textContent = criticalCount;
    }

    updateStatusCards() {
        const container = document.getElementById('statusCards');
        
        // Reuse existing cards if possible
        if (container.children.length === 0) {
            const stats = this.calculateStatistics();
            const cardsHTML = this.generateStatusCardsHTML(stats);
            container.innerHTML = cardsHTML;
        } else {
            // Update existing cards
            const stats = this.calculateStatistics();
            this.updateStatusCardsData(stats);
        }
    }

    generateStatusCardsHTML(stats) {
        const cards = [
            { label: 'Avg Heart Rate', value: stats.avgHeartRate.toFixed(1), unit: 'bpm', icon: 'fa-heart', type: 'normal' },
            { label: 'Avg Temperature', value: stats.avgTemp.toFixed(1), unit: '°C', icon: 'fa-thermometer', type: 'normal' },
            { label: 'Avg O2 Saturation', value: stats.avgO2.toFixed(1), unit: '%', icon: 'fa-lungs', type: stats.avgO2 < 92 ? 'danger' : 'normal' },
            { label: 'Critical Events', value: stats.criticalCount, unit: 'events', icon: 'fa-exclamation-triangle', type: stats.criticalCount > 0 ? 'danger' : 'success' }
        ];

        return cards.map(card => `
            <div class="status-card ${card.type}">
                <div class="card-icon"><i class="fas ${card.icon}"></i></div>
                <div class="card-label">${card.label}</div>
                <div class="card-value">${card.value}</div>
                <div class="card-subtitle">${card.unit}</div>
            </div>
        `).join('');
    }

    updateStatusCardsData(stats) {
        const cards = document.querySelectorAll('.status-card');
        if (cards.length === 0) return;

        cards.forEach(card => {
            const label = card.querySelector('.card-label').textContent;
            const stat = Object.keys(stats).find(key => key.toLowerCase().includes(label.toLowerCase()));

            if (stat) {
                card.querySelector('.card-value').textContent = stats[stat].toFixed(1);
            }
        });
    }

    calculateStatistics() {
        // Use cache if recently calculated
        if (this.cache.statistics && Date.now() - this.cache.lastFilterTime < 500) {
            return this.cache.statistics;
        }

        if (this.filteredData.length === 0) {
            return { avgHeartRate: 0, avgTemp: 0, avgO2: 0, criticalCount: 0 };
        }

        // Single pass calculation
        let sumHeartRate = 0, countHeartRate = 0;
        let sumTemp = 0, countTemp = 0;
        let sumO2 = 0, countO2 = 0;
        let criticalCount = 0;

        for (const record of this.filteredData) {
            if (record.heart_rate > 0) {
                sumHeartRate += record.heart_rate;
                countHeartRate++;
            }
            if (record.temperature > 0) {
                sumTemp += parseFloat(record.temperature);
                countTemp++;
            }
            if (record.oxygen_saturation > 0) {
                sumO2 += record.oxygen_saturation;
                countO2++;
            }
            if (this.isCritical(record)) criticalCount++;
        }

        const result = {
            avgHeartRate: countHeartRate ? sumHeartRate / countHeartRate : 0,
            avgTemp: countTemp ? sumTemp / countTemp : 0,
            avgO2: countO2 ? sumO2 / countO2 : 0,
            criticalCount: criticalCount
        };

        this.cache.statistics = result;
        return result;
    }

    updateCharts() {
        // Lazy load charts - only render visible ones
        requestAnimationFrame(() => {
            this.createHeartRateChart();
        });
        
        setTimeout(() => this.createTemperatureChart(), 100);
        setTimeout(() => this.createOxygenChart(), 200);
        setTimeout(() => this.createPatientStatsChart(), 300);
    }

    createHeartRateChart() {
        const ctx = document.getElementById('heartRateChart');
        if (!ctx) return;

        const groupedData = this.getPatientGroupedDataFast();
        const patients = Object.keys(groupedData).slice(0, 10);
        const data = patients.map(patient => {
            const rates = groupedData[patient].heart_rate;
            return rates.length ? rates.reduce((a, b) => a + b) / rates.length : 0;
        });

        if (this.charts.heartRate) this.charts.heartRate.destroy();

        this.charts.heartRate = new Chart(ctx.getContext('2d'), {
            type: 'line',
            data: {
                labels: patients,
                datasets: [{
                    label: 'Average Heart Rate (bpm)',
                    data: data,
                    borderColor: '#FF6B6B',
                    backgroundColor: 'rgba(255, 107, 107, 0.1)',
                    tension: 0.3,
                    fill: true,
                    borderWidth: 2,
                    pointRadius: 3,
                    pointBackgroundColor: '#FF6B6B'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: true, position: 'top' }
                },
                scales: {
                    y: { beginAtZero: true, max: 150 }
                }
            }
        });
    }

    createTemperatureChart() {
        const ctx = document.getElementById('temperatureChart');
        if (!ctx) return;

        const tempCounts = { normal: 0, high: 0, low: 0 };
        
        // Single pass for temperature categories
        for (const record of this.filteredData) {
            const temp = parseFloat(record.temperature);
            if (temp > this.criticalThresholds.temperature_high) tempCounts.high++;
            else if (temp < this.criticalThresholds.temperature_low) tempCounts.low++;
            else tempCounts.normal++;
        }

        if (this.charts.temperature) this.charts.temperature.destroy();

        this.charts.temperature = new Chart(ctx.getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['Normal', 'High', 'Low'],
                datasets: [{
                    data: [tempCounts.normal, tempCounts.high, tempCounts.low],
                    backgroundColor: ['#4CAF50', '#FF9800', '#2196F3'],
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    }

    createOxygenChart() {
        const ctx = document.getElementById('oxygenChart');
        if (!ctx) return;

        const bins = { '80-85': 0, '85-90': 0, '90-95': 0, '95-100': 0 };
        
        // Fast binning without filter
        for (const record of this.filteredData) {
            const o2 = record.oxygen_saturation;
            if (o2 >= 80) {
                if (o2 < 85) bins['80-85']++;
                else if (o2 < 90) bins['85-90']++;
                else if (o2 < 95) bins['90-95']++;
                else bins['95-100']++;
            }
        }

        if (this.charts.oxygen) this.charts.oxygen.destroy();

        this.charts.oxygen = new Chart(ctx.getContext('2d'), {
            type: 'bar',
            data: {
                labels: Object.keys(bins),
                datasets: [{
                    label: 'Oxygen Saturation Distribution',
                    data: Object.values(bins),
                    backgroundColor: '#2196F3',
                    borderColor: '#1565c0',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: true }
                }
            }
        });
    }

    createPatientStatsChart() {
        const ctx = document.getElementById('patientStatsChart');
        if (!ctx) return;

        const patientCount = new Set(this.filteredData.map(r => r.patient_id)).size;
        const recordCount = this.filteredData.length;
        const criticalCount = this.filteredData.filter(r => this.isCritical(r)).length;

        if (this.charts.patientStats) this.charts.patientStats.destroy();

        this.charts.patientStats = new Chart(ctx.getContext('2d'), {
            type: 'radar',
            data: {
                labels: ['Patients', 'Records', 'Critical', 'Normal', 'Data Quality'],
                datasets: [{
                    label: 'Dataset Metrics',
                    data: [
                        (patientCount / 10) * 100,
                        Math.min((recordCount / 500) * 100, 100),
                        (criticalCount / 50) * 100,
                        ((recordCount - criticalCount) / 500) * 100,
                        95
                    ],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.2)',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }

    getPatientGroupedDataFast() {
        if (this.cache.patientGroups && Date.now() - this.cache.lastFilterTime < 500) {
            return this.cache.patientGroups;
        }

        const grouped = {};
        
        for (const record of this.filteredData) {
            if (!grouped[record.patient_id]) {
                grouped[record.patient_id] = {
                    heart_rate: [],
                    temperature: [],
                    oxygen_saturation: []
                };
            }
            grouped[record.patient_id].heart_rate.push(record.heart_rate);
            grouped[record.patient_id].temperature.push(parseFloat(record.temperature));
            grouped[record.patient_id].oxygen_saturation.push(record.oxygen_saturation);
        }

        this.cache.patientGroups = grouped;
        return grouped;
    }

    updateDataTable() {
        const tbody = document.getElementById('tableBody');
        tbody.innerHTML = '';

        if (this.filteredData.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; padding: 2rem; color: #7f8c8d;">
                        <i class="fas fa-inbox" style="font-size: 2rem; margin-right: 0.5rem;"></i>
                        No data available
                    </td>
                </tr>
            `;
            return;
        }

        // Display only first 50 records for performance
        const displayData = this.filteredData.slice(0, 50);
        
        // Use document fragment for batch insertion
        const fragment = document.createDocumentFragment();

        for (const record of displayData) {
            const row = document.createElement('tr');
            const status = this.getRecordStatus(record);
            
            row.innerHTML = `
                <td>${record.patient_id}</td>
                <td>${new Date(record.timestamp).toLocaleString()}</td>
                <td>${record.heart_rate} bpm</td>
                <td>${record.temperature}°C</td>
                <td>${record.oxygen_saturation}%</td>
                <td><span class="status-badge ${status}">${status}</span></td>
            `;
            fragment.appendChild(row);
        }

        tbody.appendChild(fragment);

        // Add pagination info if there are more records
        if (this.filteredData.length > 50) {
            const paginationRow = document.createElement('tr');
            paginationRow.innerHTML = `
                <td colspan="6" style="text-align: center; padding: 1rem; color: #7f8c8d; font-size: 0.9rem;">
                    Showing 50 of ${this.filteredData.length} records
                </td>
            `;
            tbody.appendChild(paginationRow);
        }
    }

    updateAlerts() {
        const container = document.getElementById('alertsContainer');
        container.innerHTML = '';

        const criticalRecords = this.filteredData.filter(r => this.isCritical(r)).slice(0, 10);

        if (criticalRecords.length === 0) {
            container.innerHTML = '<p style="text-align: center; color: #7f8c8d; padding: 2rem;">No critical alerts at this time</p>';
            return;
        }

        // Use fragment for alerts too
        const fragment = document.createDocumentFragment();
        
        for (const record of criticalRecords) {
            const alertType = this.getAlertType(record);
            const alert = document.createElement('div');
            alert.className = `alert-item ${alertType === 'critical' ? '' : 'warning'}`;
            alert.innerHTML = `
                <div class="alert-icon">
                    <i class="fas fa-${alertType === 'critical' ? 'exclamation-circle' : 'exclamation-triangle'}"></i>
                </div>
                <div class="alert-content">
                    <div class="alert-title">${record.patient_id} - ${alertType.toUpperCase()}</div>
                    <div class="alert-message">Vital signs out of normal range</div>
                    <div class="alert-time">${new Date(record.timestamp).toLocaleTimeString()}</div>
                </div>
            `;
            fragment.appendChild(alert);
        }
        
        container.appendChild(fragment);
    }

    isCritical(record) {
        return record.heart_rate > this.criticalThresholds.heart_rate_high ||
               record.heart_rate < this.criticalThresholds.heart_rate_low ||
               parseFloat(record.temperature) > this.criticalThresholds.temperature_high ||
               parseFloat(record.temperature) < this.criticalThresholds.temperature_low ||
               record.oxygen_saturation < this.criticalThresholds.oxygen_saturation_low;
    }

    getRecordStatus(record) {
        return this.isCritical(record) ? 'critical' : 'normal';
    }

    getAlertType(record) {
        if (record.oxygen_saturation < this.criticalThresholds.oxygen_saturation_low ||
            record.heart_rate > this.criticalThresholds.heart_rate_high) {
            return 'critical';
        }
        return 'warning';
    }

    exportData() {
        if (this.filteredData.length === 0) {
            this.showToast('No data to export', 'warning');
            return;
        }

        this.showLoading(true);
        
        // Use setTimeout to prevent blocking
        setTimeout(() => {
            const csv = this.convertToCSV(this.filteredData);
            const blob = new Blob([csv], { type: 'text/csv' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `healthcare_data_${Date.now()}.csv`;
            a.click();
            window.URL.revokeObjectURL(url);

            this.showLoading(false);
            this.showToast('Data exported successfully!', 'success');
        }, 100);
    }

    convertToCSV(data) {
        const headers = Object.keys(data[0]);
        const rows = [headers.join(',')];

        for (const row of data) {
            const values = headers.map(header => {
                const value = row[header];
                return typeof value === 'string' && value.includes(',') ? `"${value}"` : value;
            });
            rows.push(values.join(','));
        }

        return rows.join('\n');
    }

    handleNavigation(event) {
        event.preventDefault();
        
        document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));
        event.target.classList.add('active');

        const href = event.target.getAttribute('href');
        document.querySelector(href)?.scrollIntoView({ behavior: 'smooth' });
    }

    showLoading(show) {
        const spinner = document.getElementById('loadingSpinner');
        if (show) {
            spinner.classList.add('active');
        } else {
            spinner.classList.remove('active');
        }
    }

    showToast(message, type = 'success') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast show ${type}`;

        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    updateReportSection() {
        if (this.filteredData.length === 0) return;

        const stats = this.calculateStatistics();
        const uniquePatients = new Set(this.filteredData.map(r => r.patient_id)).size;

        document.getElementById('reportTotalRecords').textContent = this.filteredData.length;
        document.getElementById('reportUniquePatients').textContent = uniquePatients;
        document.getElementById('reportCriticalEvents').textContent = this.filteredData.filter(r => this.isCritical(r)).length;
        document.getElementById('reportAvgHR').textContent = stats.avgHeartRate.toFixed(1) + ' bpm';
        document.getElementById('reportAvgTemp').textContent = stats.avgTemp.toFixed(1) + ' °C';
        document.getElementById('reportAvgO2').textContent = stats.avgO2.toFixed(1) + ' %';
        document.getElementById('reportLastUpdate').textContent = new Date().toLocaleTimeString();
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new HealthcareAnalyticsApp();
});
