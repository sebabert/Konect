// Formations
const educationForm = document.getElementsByClassName("education-form");
const mainEducationForm = document.querySelector("#educations-form");
const addEducationFormBtn = document.querySelector("#add-education-form-btn");
const educationsTotalForms = document.getElementById("id_education-TOTAL_FORMS");

let educationsFormCount = educationForm.length - 1;

if (addEducationFormBtn) {
    addEducationFormBtn.addEventListener("click", function (event) {
        event.preventDefault();

        const newEducationForm = educationForm[0].cloneNode(true);

        const formRegex = RegExp(`education-(\\d){1}-`, 'g');
        educationsFormCount++;

        newEducationForm.innerHTML = newEducationForm.innerHTML.replace(formRegex, `education-${educationsFormCount}-`);
        mainEducationForm.insertBefore(newEducationForm, addEducationFormBtn);
        educationsTotalForms.setAttribute('value', `${educationsFormCount + 1}`);
    });

    mainEducationForm.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-education-form-btn")) {
            event.preventDefault();
            if (educationsFormCount) {
                event.target.parentElement.remove();
                educationsFormCount--;
                updateForms();
                educationsTotalForms.setAttribute('value', `${educationsFormCount + 1}`);
            }
        }
    });
}
// Expériences
const experienceForm = document.getElementsByClassName("experience-form");
const mainExperienceForm = document.querySelector("#experiences-form");
const addExperienceFormBtn = document.querySelector("#add-experience-form-btn");
const experiencesTotalForms = document.getElementById("id_experience-TOTAL_FORMS");

let experiencesFormCount = experienceForm.length - 1;
if (addExperienceFormBtn) {
    addExperienceFormBtn.addEventListener("click", function (event) {
        event.preventDefault();

        const newExperienceForm = experienceForm[0].cloneNode(true);

        const formRegex = RegExp(`experience-(\\d){1}-`, 'g');
        experiencesFormCount++;

        newExperienceForm.innerHTML = newExperienceForm.innerHTML.replace(formRegex, `experience-${experiencesFormCount}-`);
        mainExperienceForm.insertBefore(newExperienceForm, addExperienceFormBtn);
        experiencesTotalForms.setAttribute('value', `${experiencesFormCount + 1}`);
    });

    mainExperienceForm.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-experience-form-btn")) {
            event.preventDefault();
            if (experiencesFormCount) {
                event.target.parentElement.remove();
                experiencesFormCount--;
                updateForms();
                experiencesTotalForms.setAttribute('value', `${experiencesFormCount + 1}`);
            }
        }
    });

    function updateForms() {
        let count = 0;
        for (let form of experienceForm) {
            const formRegex = RegExp(`experience-(\\d){1}-`, 'g');
            form.innerHTML = form.innerHTML.replace(formRegex, `experience-${count++}-`)
        }
    }
}
// Compétences
const skillForm = document.getElementsByClassName("skill-form");
const mainSkillForm = document.querySelector("#skills-form");
const addSkillFormBtn = document.querySelector("#add-skill-form-btn");
const skillsTotalForms = document.getElementById("id_skills-TOTAL_FORMS");

let skillsFormCount = skillForm.length - 1;

if (addSkillFormBtn) {
    addSkillFormBtn.addEventListener("click", function (event) {
        event.preventDefault();

        const newSkillForm = skillForm[0].cloneNode(true);

        const formRegex = RegExp(`skills-(\\d){1}-`, 'g');
        skillsFormCount++;

        newSkillForm.innerHTML = newSkillForm.innerHTML.replace(formRegex, `skills-${skillsFormCount}-`);
        mainSkillForm.insertBefore(newSkillForm, addSkillFormBtn);
        skillsTotalForms.setAttribute('value', `${skillsFormCount + 1}`);
    });

    mainSkillForm.addEventListener("click", function (event) {
        if (event.target.classList.contains("delete-skill-form-btn")) {
            event.preventDefault();
            if (skillsFormCount) {
                event.target.parentElement.remove();
                skillsFormCount--;
                updateForms();
                skillsTotalForms.setAttribute('value', `${skillsFormCount + 1}`);
            }
        }
    });

    function updateForms() {
        let count = 0;
        for (let form of skillForm) {
            const formRegex = RegExp(`skills-(\\d){1}-`, 'g');
            form.innerHTML = form.innerHTML.replace(formRegex, `skills-${count++}-`)
        }
    }
}
// labels
var
    $form = $("form"),
    $input = $("form input:not(:checkbox, :file)"),
    $submit = $("button[type=submit]")
;

$input.on('focus', function() {
    var $label = $("label[for='" + this.id + "']");
    $label.removeClass("form-label--hide").addClass('form-label--active-js');
});

$input.on('blur', function() {
    var $label = $("label[for='" + this.id + "']");
    $label.removeClass("form-label--active-js").addClass('form-label--hide');
});

$("section.main-section-element").on("click", function () {
    var
        $form = $("form"),
        $input = $("form input:not(:checkbox, :file)"),
        $submit = $("button[type=submit]")
    ;
    $input.on('focus', function() {
        var $label = $("label[for='" + this.id + "']");
        $label.removeClass("form-label--hide").addClass('form-label--active-js');
    });

    $input.on('blur', function() {
        var $label = $("label[for='" + this.id + "']");
        $label.removeClass("form-label--active-js").addClass('form-label--hide');
    });
});
