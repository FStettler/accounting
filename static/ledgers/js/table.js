// SUBMIT FUNCTION
window.onload = function() {
  sumTableInputs()
}
function deleteRow(table, row) {
  event.preventDefault();
  var rowIndex = row.rowIndex;
  table.deleteRow(rowIndex);
  sumTableInputs();
}


  const form = document.getElementById("my-form");
  const table = document.getElementById("info");
  const tableDataInput = document.getElementById("table-data");

  function addInputEventListeners() {
    var inputs = table.getElementsByTagName('input');
    for (var i = 0; i < inputs.length; i++) {
      if (inputs[i].type == 'number') {
        inputs[i].addEventListener('blur', sumTableInputs);
      }
    }
  }

  addInputEventListeners(); // Call the function initially

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const tbody = table.querySelector("tbody");
    const rows = tbody.querySelectorAll("tr");
    const tableData = [];
    const balance = document.getElementById("total");
    const balance_control = balance.innerHTML; 


    rows.forEach((row) => {
      const select_cells = row.querySelectorAll("select");
      const account = select_cells[0].value;

      const input_cells = row.querySelectorAll("input");
      const amount = input_cells[0].value;


      if (account && amount) {
        tableData.push({ account, amount });
      }
    });

    function myFunction(message) {
      alert(message);
    }

    if (balance_control != "0" || balance_control == ""){
      myFunction("Ledger not balancing");
    } else{
      tableDataInput.value = JSON.stringify(tableData);
      form.submit();
  }

  });

  // AFTER UPDATE FUNCTION
  function sumTableInputs() {
    var inputs = table.getElementsByTagName('input');
    var sum = 0;
    for (var i = 0; i < inputs.length; i++) {
      if (inputs[i].type == 'number') {
        sum += Number(inputs[i].value);
      }
    }
    document.getElementById('total').innerHTML = sum;
  }

  // ADD LINE - DELETE LINE FUNCTIONS

  const addRowButton = document.getElementById("add-row-button");
  addRowButton.addEventListener("click", addRow);
  // const deleteRowButton = document.getElementsById("delete-row-button");
  // deleteRowButton[0].addEventListener("click", deleteRow);
  // deleteRowButton[1].addEventListener("click", deleteRow);


  function addRow() {
    event.preventDefault();
    cols = 2
    const tbody = table.querySelector("tbody");
    var addRowButtonCellIndex = tbody.rows.length;
    var row = tbody.insertRow(addRowButtonCellIndex);
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

    var deleteRowButtonCell = row.insertCell();
    var deleteRowButton = document.createElement("button");
    deleteRowButton.textContent = "Delete row";
    deleteRowButton.onclick = function() { deleteRow(table, row); };
    deleteRowButtonCell.appendChild(deleteRowButton);

    addInputEventListeners(); // Call the function to add the event listener to the new input elements
  }


  

// }