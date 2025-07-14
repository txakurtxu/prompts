function js_init()  {
    var TAarray = document.getElementsByClassName("tarea");
    TAarray[0].value = DEFAULT_PROMPT;
    TAarray[2].value = DEFAULT_SCHEMA;
    for(var i = 0; i < TAarray.length; i++) {
        if([2, 3, 4].includes(i))    {
            TAarray[i].style.whiteSpace = "pre";
        }
        TAarray[i].addEventListener("keyup", function(e) {
            var tar = e.target;
            if(e.keyCode === 27)    {
                if(tar.style.whiteSpace === "" || tar.style.whiteSpace === "pre-line")    {
                    tar.style.whiteSpace = "pre";
                }   else    {
                    tar.style.whiteSpace = "pre-line";
                }
            }
        });
        if([0].includes(i))    {
            TAarray[i].prompt = 0;
            TAarray[i].addEventListener("keyup", function(e) {
                var tar = e.target;
                var tas = document.getElementsByClassName("tarea")[2];
                if(e.keyCode === 113)    {
                    var npro = 1;
                    if(typeof TEST_PROMPTS !== 'undefined') {
                        npro += TEST_PROMPTS.length;
                    }
                    tar.prompt = (tar.prompt + 1) % npro;
                    if(tar.prompt === 0) {
                        tar.value = DEFAULT_PROMPT;
                        tas.value = DEFAULT_SCHEMA;
                    }   else    {
                        tar.value = TEST_PROMPTS[tar.prompt - 1];
                        tas.value = TEST_SCHEMAS[tar.prompt - 1];
                    }
                }
            });
        }
    }
    var SEarray = document.getElementsByClassName("sel");   
    var INarray = document.getElementsByClassName("inp");
    var SEconst = [GPT_MODELS, GEMINI_MODELS];
    for(var i = 0; i < SEarray.length; i++) {
        if(i >= SEconst.length)    {
            SEarray[i].style.visibility = "hidden";
            INarray[i].style.visibility = "hidden";
            continue;
        }
        for(var j = 0; j < SEconst[i].length; j++)   {
            SEarray[i].options[SEarray[i].length] = new Option(SEconst[i][j], j);
        }
        INarray[i]._index = i;
        INarray[i].addEventListener("keyup", function(e)   {
            var tmp_text = INarray[e.target._index].value;
            var tmp_ind = SEconst[e.target._index].indexOf(tmp_text.toLowerCase());
            SEarray[e.target._index].selectedIndex = tmp_ind;
            if(tmp_ind !== -1)  {
                INarray[e.target._index].value = SEconst[e.target._index][SEarray[e.target._index].selectedIndex];
            }
        });
        INarray[i].value = SEconst[i][SEarray[i].selectedIndex];
        SEarray[i]._index = i;
        SEarray[i].addEventListener("change", function(e)   {
            INarray[e.target._index].value = SEconst[e.target._index][SEarray[e.target._index].selectedIndex];
        });
    }
    var BUarray = document.getElementsByClassName("but");
    for(var i = 0; i < BUarray.length; i++) {
        BUarray[i]._index = i;
        BUarray[i].addEventListener("click", sel_model);
    }
}

function sel_model(e)    {
    var tmp_ind = e.target._index;
    if([0, 2].includes(tmp_ind))    {
        run_model(0);
    }
    if([1, 2].includes(tmp_ind))    {
        run_model(1);
    }
}

async function run_model(n) {
    var tapr = document.getElementById("tapr").value;
    var tach = document.getElementById("tach").value;
    var tasc = document.getElementById("tasc").value;

    var tmp_mod = document.getElementsByClassName("inp")[n].value;
    var tmp_tar = document.getElementsByClassName("tarea")[n + 3];
    if(document.getElementsByClassName("but")[n].disabled == false)    {
        document.getElementsByClassName("but")[n].disabled = true;
    }   else    {
        return;
    }
    tmp_tar.value = "";
    tmp_tar.style.background = "rgba(240, 235, 230, 1)";

    const response = await fetch("/process", {
        method: "POST",
        headers: {  "Content-type": "application/json",
        },
        body: JSON.stringify({ 'seva': n,
            'mova': tmp_mod,
            'tapr': tapr,
            'tach': tach,
            'tasc': tasc
        }),
    });
    const reader = response.body.getReader();
    let output = "";
    while(true) {
        const {done, value} = await reader.read();
        output += new TextDecoder().decode(value);
        document.getElementsByClassName("tarea")[n + 3].value = output;
        if(done)    {
            document.getElementsByClassName("but")[n].disabled = false;
            tmp_tar.style.background = "white";
            return;
        }
    }
}
