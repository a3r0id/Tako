window.pingIndicator = (ping) => {
  var data = [
    {
      domain: { x: [0, 1], y: [0, 1] },
      value: ping,
      title: { text: "Backend Ping (MS)" },
      type: "indicator",
      mode: "number+gauge+delta",
      delta: { reference: stats.lastPing },
      gauge: { axis: { range: [0, 300] } }
    }
  ];
  
  var layout = { width: 300, height: 300 };

  Plotly.newPlot('ping-indicator', data, layout);

  stats.lastPing = ping;
}