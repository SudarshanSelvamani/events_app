    
    const addMoreBtn = document.getElementById('add_more')
    const totalNewForms = document.getElementById("id_time_set-TOTAL_FORMS")
    
    addMoreBtn.addEventListener('click',add_more_form)
    

    function add_more_form(args){
        console.log(args)
        if (event){
            event.preventDefault()
        }
        const currentTimeForms = document.getElementsByClassName('time_form')
        const currentFormCount = currentTimeForms.length
        const formCopyTarget = document.getElementById('time_form_list')
        const copyemptyForm = document.getElementById('empty_form').cloneNode(true)
        copyemptyForm.setAttribute('class','time_form')
        copyemptyForm.setAttribute('id',`form-${currentFormCount}`)
        const regex = new RegExp('__prefix__', 'g')
        copyemptyForm.innerHTML = copyemptyForm.innerHTML.replace(regex,
        currentFormCount)
        totalNewForms.setAttribute('value', currentFormCount + 1)
        formCopyTarget.append(copyemptyForm)

    }
