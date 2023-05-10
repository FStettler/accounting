window.onload = function() {

    const form = document.getElementById("my-form");
    const table = document.getElementById("info");
    const tableDataInput = document.getElementById("table-data");
  
    form.addEventListener("submit", (event) => {
      event.preventDefault();
    
      const tbody = table.querySelector("tbody");
      const rows = tbody.querySelectorAll("tr");
      const tableData = [];
    
      rows.forEach((row) => {
        const select_cells = row.querySelectorAll("select");
        const account = select_cells[0].value;

        const input_cells = row.querySelectorAll("input");
        const amount = input_cells[0].value;

    
        if (account && amount) {
          tableData.push({ account, amount });
        }
      });
    
      tableDataInput.value = JSON.stringify(tableData);
      form.submit();
    });
  
  }
  
  const addRowButton = document.getElementById("add-row-button");
  addRowButton.addEventListener("click", addRow);
  const table = document.getElementById("info").getElementsByTagName('tbody')[0]

  function addRow() {
      cols = 2
      //table = document.getElementById("info").getElementsByTagName('tbody')[0]
        // Get the index of the "Add Row" button cell
      var addRowButtonCellIndex = table.rows.length;
  
      // Add a new row
      var row = table.insertRow(addRowButtonCellIndex);
  
      // Add the cells to the new row
        var cell = row.insertCell();
        cell.innerHTML = "<select  name='credit_account'>\
            <option>Cash</option>\
            <option>Bank</option>\
            <option>Debtors</option>\
            <option>Creditors</option>\
            <option>Sales</option>\
            <option>Purchases</option>\
            <option>Capital</option>\
        </select>";
  
        var cell = row.insertCell();
        cell.innerHTML = "<input type='number' name='amount'>";
  
  
  
      // Add a new "Delete Row" button cell
      var deleteRowButtonCell = row.insertCell();
      var deleteRowButton = document.createElement("button");
      deleteRowButton.textContent = "Delete line";
      deleteRowButton.onclick = function() { deleteRow(table, row); };
      deleteRowButtonCell.appendChild(deleteRowButton);
  }
  
  function deleteRow(table, row) {
  // Get the index of the row to delete
  var rowIndex = row.rowIndex;
  
  // Remove the row
  table.deleteRow(rowIndex);
  }
