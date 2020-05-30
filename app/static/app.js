function openResponse(){

    console.log("hi");
    const responseDiv = document.getElementById("response");

    if(responseDiv.style.display === ""){
        responseDiv.style.display = "flex";
        console.log("openning");
    }
    else{
        console.log("closing");
    }
}
 
