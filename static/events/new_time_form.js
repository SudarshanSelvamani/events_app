    
    function clone_time_form(currentFormCount){
        const copyemptyForm = document.getElementById('empty_form').cloneNode(true)
        copyemptyForm.setAttribute('class','time_form')
        copyemptyForm.setAttribute('id',`form-${currentFormCount}`)
        return copyemptyForm
    }

    function place_in_time_form_class(){
        const currentTimeForms = document.getElementsByClassName('time_form')
        const currentFormCount = currentTimeForms.length
        return currentFormCount
    }
    
    function replace_form_count(){
        const regex = new RegExp('__prefix__', 'g')
        copyemptyForm.innerHTML = copyemptyForm.innerHTML.replace(regex,
        currentFormCount)
    }

    const addMoreBtn = document.getElementById('add_more')
    const totalNewForms = document.getElementById("id_time_set-TOTAL_FORMS")
    
    addMoreBtn.addEventListener('click',add_more_form)
    

    function add_more_form(args){
        console.log(args)
        if (args){
            args.preventDefault()
        }
        const formCopyTarget = document.getElementById('time_form_list')
        currentFormCount = place_in_time_form_class()
        copyemptyForm = clone_time_form(currentFormCount)
        replace_form_count()
        totalNewForms.setAttribute('value', currentFormCount + 1)
        formCopyTarget.append(copyemptyForm)
    }
