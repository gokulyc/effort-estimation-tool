console.log("Running");

document.addEventListener("DOMContentLoaded", () => {
    console.log("Running on page loaded");
    let task_type = document.getElementById("task_type");
    let task_size = document.getElementById("size");
    let task_estimate_alert = document.getElementById("task_estimate_alert");
    console.log(task_estimate_alert.style.display)
    task_estimate_alert.style.display = "none"
    task_type.addEventListener("blur", fetchMetrics);
    task_size.addEventListener("blur", fetchMetrics);


});

const fetchMetrics = () => {
    let task_type = document.getElementById("task_type").value;
    let task_size = document.getElementById("size").value;
    let task_estimate_alert = document.getElementById("task_estimate_alert");

    console.log(task_type);
    console.log(task_size);

    fetch("/fetch_time_estimate", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            task_type, task_size
        })
    }).then(res => {
        if (res.ok) {
            task_estimate_alert.style.display = ""
            return res.json()
        } else {
            return res.text()
        }
    }).then(res => {
        console.log(res);
        if (res.message == "Not enough data") {
            setTaskEstimateAlertMsg(null, false)
        } else {
            setTaskEstimateAlertMsg(res.data, true);
        }


    }).catch(err => console.log(`Err: ${err}`))
}

const setTaskEstimateAlertMsg = (response, isEnoughDataAvailable = false) => {
    let task_message = document.getElementById("task_message");
    if (isEnoughDataAvailable) {
        task_message.innerText = `estimated_effort : ${response.estimated_effort} (Hrs) | confidence_level : ${response.confidence_level} | range : ${response.range}`

    } else {
        task_message.innerText = `Enough data not available to calculate estimated_effort.`
    }
}