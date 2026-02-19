var myChart = null;
var currentPoint = null;

$(document).ready(function() {
    // FORCE UNCHECK ON LOAD
    $('#filterWritable').prop('checked', false);

    // Initialize DataTable (English)
    var table = $('#pointsTable').DataTable({ 
        "pageLength": 25,
        "language": { 
            "search": "Search attributes:",
            "lengthMenu": "Show _MENU_ entries",
            "info": "Showing _START_ to _END_ of _TOTAL_ attributes",
            "paginate": { "next": "Next", "previous": "Previous" }
        },
        "order": [[ 0, "desc" ]] 
    });

    // Filter Logic
    $('#filterWritable').on('change', function() {
        var label = $(this).closest('.custom-toggle-box').find('.toggle-label');
        if (this.checked) {
            label.css('color', '#3182ce');
            $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
                return $(table.row(dataIndex).node()).hasClass('writable-row');
            });
        } else {
            label.css('color', '#4a5568');
            $.fn.dataTable.ext.search.pop();
        }
        table.draw();
    });

    // Individual Refresh (Event Delegation)
    $(document).on('click', '.refresh-btn', function(e) {
        e.stopPropagation(); 
        var btn = $(this);
        var pid = btn.data('id');
        var valSpan = $('#val-' + pid);
        btn.find('i').addClass('fa-spin');
        valSpan.addClass('updating');

        $.get('/get_point/' + pid, function(data) {
            if (data && data.display !== "N/A") {
                valSpan.text(data.display).removeClass('updating');
                $('#row-' + pid).attr('data-details', JSON.stringify(data.raw));
                valSpan.css('color', '#48bb78'); 
                setTimeout(function() { valSpan.css('color', ''); }, 1000);
            }
        }).always(function() { 
            btn.find('i').removeClass('fa-spin'); 
            valSpan.removeClass('updating'); 
        });
    });

    // Open Modal
    $(document).on('click', '#pointsTable tbody tr', function() {
        var detailsAttr = $(this).attr('data-details');
        if (!detailsAttr) return;

        var data = JSON.parse(detailsAttr);
        currentPoint = data;
        var meta = data.metadata;
        var valObj = data.value || data.datavalue;
        var div = meta.divisor || 1;
        
        // Fill UI
        $('#tCurrentValue').text((valObj.integerValue / div).toFixed(meta.decimal || 1));
        $('.modal-unit').text(meta.unit || "");
        $('#modalTitle').text(data.title);
        $('#tType').text(meta.variableType + " (" + meta.variableSize + ")");
        $('#tRange').text((meta.minValue/div) + " - " + (meta.maxValue/div));
        $('#tDiv').text(div + " / " + meta.decimal);
        $('#tMod').text(meta.modbusRegisterID);
        $('#tDesc').text(data.description || "No description available.");
        
        // API Info
        var cleanUrl = window.location.origin.replace(':5000', ':8443') + "/api/v1/devices/0/points/" + meta.variableId;
        $('#tEndpoint').text(cleanUrl);

        // JSON Payload
        var payload = [{"type": "datavalue", "variableId": meta.variableId, "integerValue": valObj.integerValue}];
        $('#payloadExample').text(JSON.stringify(payload, null, 2));

        if (meta.isWritable) {
            $('#writeSection').show();
            $('#tMethodWrite').show();
            $('#newValueInput').val(valObj.integerValue / div);
            $('#rangeHint').text(`Allowed hardware range: ${meta.minValue/div} to ${meta.maxValue/div}`);
            $('#modalHeader').attr('class', 'modal-header bg-primary text-white py-2');
        } else {
            $('#writeSection').hide();
            $('#tMethodWrite').hide();
            $('#modalHeader').attr('class', 'modal-header bg-secondary text-white py-2');
        }

        new bootstrap.Modal(document.getElementById('detailModal')).show();
        loadChart(meta.variableId, data.title, meta.unit);
    });

    // Save Change
    $('#saveBtn').click(function() {
        var newVal = parseFloat($('#newValueInput').val());
        var rawVal = Math.round(newVal * (currentPoint.metadata.divisor || 1));
        $(this).prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Saving...');

        $.ajax({
            url: '/update', 
            method: 'POST', 
            contentType: 'application/json',
            data: JSON.stringify({ pid: currentPoint.metadata.variableId, raw_val: rawVal }),
            success: function() { location.reload(); },
            error: function() { 
                alert('Error: Could not save setting.'); 
                $('#saveBtn').prop('disabled', false).text('Save Change'); 
            }
        });
    });
});

function loadChart(pid, title, unit) {
    if (myChart) myChart.destroy();
    $.get('/get_history/' + pid, function(res) {
        var ctx = document.getElementById('historyChart').getContext('2d');
        myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: res.labels,
                datasets: [{ 
                    label: title + ' (' + unit + ')', 
                    data: res.values, 
                    borderColor: '#3182ce', 
                    tension: 0.3, 
                    fill: true, 
                    backgroundColor: 'rgba(49, 130, 206, 0.05)' 
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    });
}
