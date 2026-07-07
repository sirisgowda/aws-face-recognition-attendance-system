const REGISTER_API =
"https://YOUR_API_GATEWAY/register";

const ATTENDANCE_API =
"https://YOUR_API_GATEWAY/attendance";

const EMPLOYEE_API =
"https://YOUR_API_GATEWAY/employees";


async function registerEmployee(){

    document.getElementById("output").innerHTML =
    "Launching registration...";

}


async function recognizeEmployee(){

    document.getElementById("output").innerHTML =
    "Launching face recognition...";

}


async function loadAttendance(){

    try{

        const response = await fetch(ATTENDANCE_API);

        const data = await response.json();

        document.getElementById("output").innerHTML =
            JSON.stringify(data,null,2);

    }

    catch(err){

        document.getElementById("output").innerHTML =
        err;

    }

}