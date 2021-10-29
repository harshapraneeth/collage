// --------- loading html elements

const target_canvas = document.getElementById("target_canvas");
const inputs_canvas = document.getElementById("inputs_canvas");
const output_canvas = document.getElementById("output_canvas");
const target_image = document.getElementById("target_image");
const input_images = document.getElementById("input_images");
const output_size = document.getElementById("output_size");
const output_size_display = document.getElementById("output_size_display");
const cell_size = document.getElementById("cell_size");
const cell_size_display = document.getElementById("cell_size_display");
const overlay_opacity = document.getElementById("overlay_opacity");
const overlay_opacity_display = document.getElementById("overlay_opacity_display");
const target_context = target_canvas.getContext("2d");
const inputs_context = inputs_canvas.getContext("2d");
const output_context = output_canvas.getContext("2d");
const log = document.getElementById("log");

// --------- global variables
var output_size_value = output_size.value;
var cell_size_value = cell_size.value;
var overlay_opacity_value = overlay_opacity.value;
var n_cell_rows, n_cell_cols;

var file;
var input_files;
const reader = new FileReader();
const image = new Image();

var target_avg;
var input_avgs;
var input_images_array;
var output_image;

// --------- event handlers

output_size.oninput = () => {
    output_size_display.innerHTML = output_size.value;
};

cell_size.oninput = () => {
    cell_size_display.innerHTML = cell_size.value;
};

overlay_opacity.oninput = () => {
    overlay_opacity_display.innerHTML = overlay_opacity.value;
};

output_size.onchange = () => {
    output_size_value = output_size.value;
};

cell_size.onchange = () => {
    cell_size_value = cell_size.value;
};

overlay_opacity.onchange = () => {
    overlay_opacity_value = overlay_opacity_value.value;
};

target_image.onchange = e => {
    file = e.target.files[0];
};

input_images.onchange = e => {
    input_files = e.target.files;
    n_images = input_files.length;
    input_images_array = new Array(n_images);
    input_avgs = new Array(n_images);
};

image.onload = () => {
    let height = image.height;
    let width = image.width;

    if(height<output_size_value)
    {
        width =  Math.round(width*output_size_value/height);
        height = output_size_value;
    }

    if(width<output_size_value)
    {
        height = Math.round(height*output_size_value/width);
        width = output_size_value;
    }

    n_cell_rows = Math.round(height/cell_size_value);
    n_cell_cols = Math.round(width/cell_size_value);

    target_canvas.height = n_cell_rows;
    target_canvas.width = n_cell_cols;

    target_context.save();
    target_context.translate(n_cell_cols/2, n_cell_rows/2);
    target_context.rotate(-90*Math.PI/180.0);
    target_context.scale(-1, 1);
    target_context.translate(-n_cell_cols/2, -n_cell_rows/2);
    target_context.drawImage(image, 0, 0, n_cell_cols, n_cell_rows);
    target_context.restore();
    target_avg = target_context.getImageData(0, 0, n_cell_cols, n_cell_rows).data;
    log.innerHTML += "Loading the Target image... Done <br>";
};

reader.onload = event => {
    image.src = event.target.result;
};

// --------- main functions

function init()
{
    log.innerHTML = "Loading the Target image... <br>";
    reader.readAsDataURL(file);
    load_images()
}

function load_images()
{
    log.innerHTML += "Loading the Input images... <br>";

    const filereader = new FileReader();
    const input_image = new Image();
    let x = 0, n = cell_size_value*cell_size_value*4;

    input_image.onload = () => {
        inputs_context.drawImage(input_image, 0, 0, cell_size_value, cell_size_value);
        input_images_array[x] = inputs_context.getImageData(0, 0, cell_size_value, cell_size_value);

        input_avgs[x] = [0, 0, 0];
        
        let i = 0;
        while(i<n)
        {
            input_avgs[x][0] += input_images_array[x].data[i];
            input_avgs[x][1] += input_images_array[x].data[i+1];
            input_avgs[x][2] += input_images_array[x].data[i+2];
            i += 4;
        }

        input_avgs[x][0] = input_avgs[x][0]*3/n;
        input_avgs[x][1] = input_avgs[x][1]*3/n;
        input_avgs[x][2] = input_avgs[x][2]*3/n;

        x++;
        if(x<n_images) filereader.readAsDataURL(input_files[x]);
        else
        {
            log.innerHTML += "Loading the Input images... Done <br>";
            generate();
        }
    };

    filereader.onload = e => {
        input_image.src = e.target.result;
    };

    filereader.readAsDataURL(input_files[0]);
}

function generate()
{
    log.innerHTML += "Generating Collage... <br>";;
    let row = 0, col = 0, n = n_cell_rows*n_cell_cols*cell_size_value*cell_size_value*4;

    output_canvas.height = n_cell_rows*cell_size_value;
    output_canvas.width = n_cell_cols*cell_size_value;

    let j = 0;
    while(j<n_cell_cols*n_cell_rows*4)
    {
        let min_d = Infinity, min_i = -1;
        for(let k=0;k<n_images;k++)
        {
            d = Math.abs(target_avg[j]-input_avgs[k][0])+
                Math.abs(target_avg[j+1]-input_avgs[k][1])+
                Math.abs(target_avg[j+2]-input_avgs[k][2]);
            if(d<min_d)
            {
                min_d = d;
                min_i = k;
            }
        }
        j+=4;

        output_context.putImageData(input_images_array[min_i], row*cell_size_value, col*cell_size_value);
        col++;
        if(col>=n_cell_cols)
        {
            row++;
            col = 0;
        }
    }
    
    put_overlay();

    rescale(output_canvas);

    log.innerHTML += "Generating Collage... Done<br>";
}

function put_overlay()
{
    target_canvas.height = n_cell_rows*cell_size_value;
    target_canvas.width = n_cell_cols*cell_size_value;
    target_context.drawImage(image, 0, 0, target_canvas.width, target_canvas.heigt);

    let overlay_data = target_context.getImageData(0, 0, target_canvas.width, target_canvas.height);
    let output_data = output_context.getImageData(0, 0, target_canvas.width, target_canvas.height);
    let n = target_canvas.height*target_canvas.width*4;
    let o = overlay_opacity_value/100;

    console.log(overlay_data.data);

    for(let i=0;i<n;i+=4)
    {
        output_data.data[i] = Math.round(o*overlay_data.data[i] + (1-o)*output_data.data[i]);
        output_data.data[i+1] = Math.round(o*overlay_data.data[i+1] + (1-o)*output_data.data[i+1]);
        output_data.data[i+2] = Math.round(o*overlay_data.data[i+2] + (1-o)*output_data.data[i+2]);
    }

    output_context.putImageData(output_data, 0, 0);
}

function rescale(elem)
{
    var width = elem.offsetWidth;
    var height = elem.offsetHeight;
    var windowWidth = window.innerWidth;
    var windowHeight = window.innerHeight;
    var r = 1;
    r = Math.min(1, Math.min(windowWidth / width, windowHeight / height));

    elem.setAttribute("style", "zoom: "+r);
}

function saveImage()
{
    const link = document.createElement("a");
    link.download = "collage.png";
    link.innerHTML = "Download File";
    link.href = output_canvas.toDataURL("image/png").replace("image/png", "image/octet-stream");
    
    if (window.webkitURL == null) 
    {
        // Firefox requires the link to be added to the DOM
        // before it can be clicked.
        link.onclick = destroyClickedElement;
        link.style.display = "none";
        document.body.appendChild(link);
    }

    link.click();
}