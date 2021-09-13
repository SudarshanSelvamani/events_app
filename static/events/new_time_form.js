    
    function clone_time_form(currentFormCount){
        const copyemptyForm = document.getElementById('empty_form').cloneNode(true)
        copyemptyForm.setAttribute('class','time_form')
        copyemptyForm.setAttribute('id',`form-${currentFormCount}`)
        return copyemptyForm
    }

    function get_time_form_class(){
        const currentTimeForms = document.getElementsByClassName('time_form')
        const currentFormCount = currentTimeForms.length
        return currentFormCount
    }
    
    function update_time_form_count(){
        const regex = new RegExp('__prefix__', 'g')
        console.log(regex)
        clonedTimeForm.innerHTML = clonedTimeForm.innerHTML.replace(regex,
        currentFormCount)
    }

    const addMoreBtn = document.getElementById('add_more')
    const totalNewForms = document.getElementById("id_time_set-TOTAL_FORMS")
    
    addMoreBtn.addEventListener('click',add_more_form)
    

    function add_more_form(events){
        events.preventDefault()
        const formCopyTarget = document.getElementById('time_form_list')
        currentFormCount = get_time_form_class()
        clonedTimeForm = clone_time_form(currentFormCount)
        formCopyTarget.append(clonedTimeForm)
        update_time_form_count()
        totalNewForms.setAttribute('value', currentFormCount + 1)
        
    }
