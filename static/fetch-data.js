document.addEventListener('DOMContentLoaded', () => {

    const ajaxSend = async (formData) => {
        const form = document.getElementById('solve-form');
        const fetchResp = await fetch(form.action, {
            method: 'POST',
            body: formData
        });
        if (!fetchResp.ok) {
            document.getElementById('result').innerHTML = '<p style="color: firebrick">Error</p>';
            console.log(fetchResp);
            throw new Error();
        }
        return await fetchResp.text();
    };

    const form = document.getElementById('solve-form');
    form.addEventListener('submit', function (e) {

        e.preventDefault();

        document.getElementById('result').innerHTML = '<div class="lds-dual-ring"></div>';

        const formData = new FormData(this);

        ajaxSend(formData)
            .then((response) => {
                var data = JSON.parse(response);
                var img = document.getElementById('plot');
                
                img.setAttribute("src", data.img);
                generateTable(data.t, data.x, data.length);
            })
            .catch((err) => {
                document.getElementById('result').innerHTML = '<p style="color: firebrick">Error</p>';
                console.error(err)
            })
    });

    generateTable = (t, x, length) => {
        let div = document.getElementById("tableResult");

        //clear already created table before
        div.innerHTML = '';

        div.classList = "container"
        t_data = t.split(',').map(Number);
        x_data = x.split(',').map(Number);

        let table = document.createElement("table");

        let tableBody = document.createElement("tbody");

        for(let i = 0; i < length; i++) {
            let row = document.createElement("tr");

            let cell = document.createElement("td");
            let cell2 = document.createElement('td');

            let cellValue = document.createTextNode(t_data[i].toFixed(5));

            let cellValue2 = document.createTextNode(x_data[i]);

            cell.appendChild(cellValue);
            cell2.appendChild(cellValue2);
            row.appendChild(cell);
            row.appendChild(cell2);
            
            tableBody.appendChild(row);
        };

        table.appendChild(tableBody);

        div.appendChild(table);
        table.setAttribute("border", "2");
    }
});