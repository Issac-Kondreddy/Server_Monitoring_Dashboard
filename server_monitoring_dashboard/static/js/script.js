window.onload = function() {
    console.log('DOM is fully loaded');

    // Function to initialize a chart
    function initChart(chartId, label, bgColor, borderColor) {
        const chartElement = document.getElementById(chartId);
        if (!chartElement) {
            console.error(`Element with id "${chartId}" not found`);
            return null;
        }

        const ctx = chartElement.getContext('2d');
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: label,
                    data: [],
                    backgroundColor: bgColor,
                    borderColor: borderColor,
                    borderWidth: 1,
                    fill: true
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Initialize all charts
    const cpuChart = initChart('cpuChart', 'CPU Usage (%)', 'rgba(255, 99, 132, 0.2)', 'rgba(255, 99, 132, 1)');
    const memoryChart = initChart('memoryChart', 'Memory Usage (%)', 'rgba(54, 162, 235, 0.2)', 'rgba(54, 162, 235, 1)');
    const diskChart = initChart('diskChart', 'Disk Usage (%)', 'rgba(75, 192, 192, 0.2)', 'rgba(75, 192, 192, 1)');
    const networkChart = initChart('networkChart', 'Network Usage (MB)', 'rgba(153, 102, 255, 0.2)', 'rgba(153, 102, 255, 1)');
    const networkSpeedChart = initChart('networkSpeedChart', 'Network Speed (MB/s)', 'rgba(255, 206, 86, 0.2)', 'rgba(255, 206, 86, 1)');
    const cpuTempChart = initChart('cpuTempChart', 'CPU Temperature (°C)', 'rgba(255, 159, 64, 0.2)', 'rgba(255, 159, 64, 1)');
    const dockerChart = initChart('dockerChart', 'Running Docker Containers', 'rgba(255, 206, 86, 0.2)', 'rgba(255, 206, 86, 1)');


    // Function to update all charts
    function updateChart(chart, data) {
        if (chart) {
            const timestamp = new Date().toLocaleTimeString();
            chart.data.labels.push(timestamp); // Add new timestamp
            chart.data.datasets[0].data.push(data); // Add new data point
            chart.update(); // Update the chart
        }
    }

    // Fetch data and update charts
    async function fetchData() {
        console.log('Fetching data...');
        try {
            // Fetch CPU Usage
            const cpuResponse = await fetch('/api/cpu/');
            const cpuData = await cpuResponse.json();
            console.log('CPU Data:', cpuData);
            document.getElementById('cpu').textContent = cpuData['CPU Storage'] + '%';
            updateChart(cpuChart, cpuData['CPU Storage']);

            // Fetch Memory Usage
            const memoryResponse = await fetch('/api/memory/');
            const memoryData = await memoryResponse.json();
            document.getElementById('memory').textContent = memoryData['Memory Usage'] + '%';
            updateChart(memoryChart, memoryData['Memory Usage']);

            // Fetch Disk Usage
            const diskResponse = await fetch('/api/disk/');
            const diskData = await diskResponse.json();
            document.getElementById('disk').textContent = diskData['Disk Usage'] + '%';
            updateChart(diskChart, diskData['Disk Usage']);

            // Fetch Network Usage
            const networkResponse = await fetch('/api/network/');
            const networkData = await networkResponse.json();
            document.getElementById('network').textContent = `Sent: ${networkData['Bytes Sent (MB)']} MB, Received: ${networkData['Bytes Received (MB)']} MB`;
            updateChart(networkChart, (networkData['Bytes Sent (MB)'] + networkData['Bytes Received (MB)']) / 2);

            // Fetch Docker Containers
            const dockerResponse = await fetch('/api/docker/');
            const dockerData = await dockerResponse.json();
            let dockerHTML = '';
            dockerData['Containers'].forEach(container => {
                dockerHTML += `<tr><td>${container.ID}</td><td>${container.Name}</td><td>${container.Status}</td></tr>`;
            });
            document.getElementById('dockerContainers').innerHTML = dockerHTML || '<tr><td colspan="3">No Containers Running</td></tr>';
            updateChart(dockerChart, dockerData['Containers'].length);

            // Fetch CPU Temperature
            const tempResponse = await fetch('/api/cpu-temp/');
            const tempData = await tempResponse.json();
            document.getElementById('cpuTemp').textContent = tempData['CPU Temperature'] + '°C';
            updateChart(cpuTempChart, tempData['CPU Temperature']);

            // Fetch Fan Speed
            const fanResponse = await fetch('/api/fan-speed/');
            const fanData = await fanResponse.json();
            document.getElementById('fanSpeed').textContent = fanData['Fan Speed'];

            // Fetch Network Speed
            const netSpeedResponse = await fetch('/api/network-speed/');
            const netSpeedData = await netSpeedResponse.json();
            console.log('Network Speed Data:', netSpeedData);  // Check the data
            document.getElementById('networkSpeed').textContent = `Upload: ${netSpeedData['Upload Speed']}, Download: ${netSpeedData['Download Speed']}`;
    

            // Fetch Top Processes
            const processResponse = await fetch('/api/processes/');
            const processData = await processResponse.json();
            console.log('Process Data:', processData);  // Check the data
    
            let processHTML = '<ul>';
            processData.forEach(process => {
                processHTML += `<li>${process.name} (PID: ${process.pid}): CPU: ${process.cpu}% | Memory: ${process.memory}%</li>`;
            });
            processHTML += '</ul>';
            document.getElementById('processes').innerHTML = processHTML;

        } catch (error) {
            console.error('Error fetching data:', error);
        }
    }

    // Fetch data when the page loads
    fetchData();
    // Refresh data every 5 seconds
    setInterval(fetchData, 5000);
};
