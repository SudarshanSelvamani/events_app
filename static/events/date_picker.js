const dateField = document.getElementById('date-picker')
dateField.addEventListener("click", openDatePicker())

const clearAll = document.getElementById('clear-filters')
clearAll.addEventListener("click",function() {clearFilters()})

function openDatePicker(){
    new Litepicker({
    element: document.getElementById('date-picker'),
    singleMode: false,
    setup: (picker) => {

      picker.on('selected', (date1, date2) => {
        console.log(date1.dateInstance.toISOString())
        const start_date = date1.dateInstance.toISOString().split('T')[0]
        const end_date = date2.dateInstance.toISOString().split('T')[0]
        updateDateInForm(start_date, end_date)
        
      });
    },
})

  }


function updateDateInForm(start_date, end_date){
  document.getElementById('id_start_from_to_time_0').value = start_date
  if(start_date != end_date){
    document.getElementById('id_start_from_to_time_1').value = end_date
  }
}

function clearFilters(){
  document.getElementById("date-picker").value = ""
  document.getElementById("id_name").value = ""
  document.getElementById('id_category').value = ""
  document.getElementById('id_place').value = ""
  document.getElementById('id_start_from_to_time_0').value = ""
  document.getElementById('id_start_from_to_time_1').value = "" 
}

