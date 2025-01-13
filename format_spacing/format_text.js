let result_box = document.getElementById("result_text");
let lyrics_panel = document.getElementById("lyrics_panel");


document.getElementById("format_text").addEventListener("click", function(){
    const raw_text = lyrics_panel.value.split("\n\n");

    let formatted_text = "<pre>";
    for (let i = 0; i < raw_text.length; i++){
        let current_raw_text = raw_text[i];
        formatted_text += current_raw_text;

        if (i !== raw_text.length-1){
            if (current_raw_text.split("\n").length % 2){
                formatted_text += "\n\n\n\n";
            } else {
                formatted_text += "\n\n\n";
            }
        }
    }
    formatted_text += "</pre>"
    result_box.innerText = formatted_text;
});