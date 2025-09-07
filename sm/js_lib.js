let CUR_PRO= DEFAULT_PROMPT;
let CUR_SCH= DEFAULT_SCHEMA;
let CUR_CAS;
let buan;

let cbody= 0;
let saved_html;

function js_init(n)  {
    buan= document.getElementById("buan");
    buan.addEventListener("click", run_model);
    document.getElementById("imkn").hidden= false;
    document.getElementById("imsm").hidden= false;
    if(n!== 0)   {
        return;
    }
    document.body.addEventListener("keyup", function(e) {
        var tar= e.target;
        if(e.keyCode=== 113)    {
            let pre_html= saved_html;
            saved_html= document.body.innerHTML;
            if(cbody=== 0)    {
                cbody= 1;
                CUR_CAS= document.getElementById("tatr").value;
                const c2= document.getElementById("c2");
                c2.innerHTML= "<textarea id=\"ta21\" style=\"display: block; width: 100%; max-width: 50rem; margin-left: auto; margin-right: auto; height: 75%; resize: none; font: inherit; border-radius: 6px;\">"+ CUR_PRO + "</textarea>";
                c2.innerHTML+= "<textarea id=\"ta22\" style=\"display: block; width: 100%; max-width: 50rem; margin-left: auto; margin-right: auto; height: 20%; resize: none; font: inherit; border-radius: 6px;\">"+ CUR_SCH + "</textarea>";
                document.getElementById("ta21").focus();
            }   else    {
                cbody= 0;
                CUR_PRO= document.getElementById("ta21").value;
                CUR_SCH= document.getElementById("ta22").value;
                document.body.innerHTML= pre_html;
                document.getElementById("tatr").value= CUR_CAS;
                document.getElementById("tatr").focus();
                js_init(1);
            }
        }
    });
    document.getElementById("tatr").focus();
}

async function run_model()  {
    if(buan.disabled== false)    {
        buan.disabled= true;
        document.getElementById("c21").hidden= true;
        document.getElementById("c21").innerHTML= "";
    }   else    {
        return;
    }
    try {
        const response= await fetch("/process", {
            method: "POST",
            headers: {  "Content-type": "application/json",
            },
            body: JSON.stringify({ 'seva': 9,
                'mova': GEMINI_MODELS[0],
                'tapr': "",
                'tach': CUR_PRO.replaceAll("XXX", document.getElementById("tatr").value),
                'tasc': CUR_SCH
            }),
        });
        if(!response.ok)    {
            console.log(`Error: ${response.status}`);
        }
        const data= await response.json();
        let colc="";
        let code= Object.values(data)[0];
        if(["rojo"].includes(code.toLowerCase()))    {
            colc= "background-color: rgba(255, 0, 0, 1); ";
        }   else if(["amarillo"].includes(code.toLowerCase()))   {
            colc= "background-color: rgba(255, 255, 0, 1); ";
        }   else if(["verde"].includes(code.toLowerCase()))   {
            colc= "background-color: rgba(0, 255, 0, 1); ";
        }   else if(["negro"].includes(code.toLowerCase()))   {
            colc= "background-color: rgba(0, 0, 0, 1); ";
        }
        let nhtml= "C&oacute;digo: "+ code+ "&nbsp;<span class=\"dot\" style=\""+ colc+ "position: absolute;\"></span> "+ "<br><br>"+ Object.values(data)[1];
        document.getElementById("c21").innerHTML= nhtml;
        document.getElementById("c21").hidden= false;

        let ccas= document.getElementById("tatr").value;
        while(ccas.length> 1 && ccas.charAt(ccas.length- 1)=== "\n")  {
            ccas= ccas.slice(0, -1);
        }
        /*ccas= ccas+ "\n\n\n";*/
        let ques= Object.values(data)[2];
        /*
        if(typeof ques!== "undefined")    {
            for(var i= 0; i< ques.length; i++)  {
                ccas+= "• "+ ques[i]+ "\n\n";
            }
        }
        */
        document.getElementById("tatr").value= ccas;
        document.getElementById("tatr").focus();
    }   catch(e)    {
        console.log("Error in showing results: "+ e);
    }
    buan.disabled= false;
}
