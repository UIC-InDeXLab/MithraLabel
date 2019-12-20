// the variable that holds the data from csv file
var ovData = [];
var cols_num = [];
var cols = [];
// var cols = ["age", "decile_score", "priors_count", "c_days_from_compas", "v_decile_score", "Violence_score", "Recidivism_score"];

// $(document).ready(function () {
//   // loadOVData("numeric_single.csv")
// });

window.onpopstate = function (event) {
  window.location.reload();
};

function load_single_meta() {
  var today = new Date();
  $.ajax({
    type: 'GET',
    url: "/api/parse_single/",
    contentType: "application/json;charset=UTF-8",
    dataType: 'json',
    success: function (dat) {
      // console.log("overview ajax back", today.getMinutes() + ":" + today.getSeconds() + ":" + today.getMilliseconds());
      // console.log("data ", dat.re);
      loadOVData(dat.re)
    }
  });
}

function loadOVData(d) {
  var today = new Date();
  // console.log("\n overview\n ", today.getMinutes() + ":" + today.getSeconds() + ":" + today.getMilliseconds());
  var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
  ovData = [];
  cols_num = [];
  cols = [];
  // d3.csv("/static/data/" + "numeric_single.csv").then(function (d) {
  ovData = d
  cols_num = [0]

  //get all column names
  var colnames = d3.keys(ovData[0]);
  colnames.forEach(function (v, i) {
    if (cols_num.indexOf(i) >= 0) {
      cols.push(v)
    }
  });
  // console.log('cols : ', cols)
  // console.log("s drawing ", today.getMinutes() + ":" + today.getSeconds() + ":" + today.getMilliseconds());
  cols.forEach(element => {
    drawRow(ovData, element);
    drawHistogram(ovData, element);
  });
  toggleHis();
  // console.log("e drawing ", today.getMinutes() + ":" + today.getSeconds() + ":" + today.getMilliseconds());
  // });
}

function drawHistogram(data, col) {

  var margin = {
      top: 20,
      right: 20,
      bottom: 40,
      left: 40
    },
    width = $(".frame").width() - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

  var map_data = data.map(function (d) {
    return Number(d[col]);
  });

  var histogram = d3.histogram()
    (map_data);

  var x = d3.scaleLinear()
    .domain(d3.extent(map_data)).nice()
    .range([margin.left, width - margin.right]);

  var histogram = d3.histogram()
    .domain(x.domain())
    .thresholds(x.ticks(60))
    (map_data);

  var y = d3.scaleLinear()
    .domain([0, d3.max(histogram, d => d.length)]).nice()
    .range([height - margin.bottom, margin.top]);

  var new_div = d3.select("#" + col + "block").append("div")
    .attr("class", "fullhis")
    .attr("id", col + "fullhis")
    .style("display", "none");

  var svg = d3.select("#" + col + "fullhis").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  var tooltip = d3.select("#" + col + "fullhis").append("div").attr("class", "toolTip");

  // bars
  svg.append("g")
    .attr("fill", "black")
    .selectAll("rect")
    .data(histogram)
    .enter().append("rect")
    .attr("class", col + "rect")
    .attr("x", d => x(d.x0) + 1)
    .attr("width", d => Math.max(0, x(d.x1) - x(d.x0)))
    .attr("y", d => y(d.length))
    .attr("height", d => y(0) - y(d.length))
    .attr("stroke", "white")
    .attr("stroke-width", "1")

    // hover interaction with tooltip
    .on("mousemove", function (d) {

      d3.selectAll("." + col + "rect").attr("opacity", "0.2");

      d3.select(this).attr("opacity", "1");

      tooltip
        .style("left", d3.event.pageX - 50 + "px")
        .style("top", d3.event.pageY - 70 + "px")
        .style("display", "inline-block")
        .html("<b>" + col + "</b> : " + (d.x0) + "-" + (d.x1) + "</br><b>Count</b> : " + (d.length));
    })
    .on("mouseout", function (d) {
      d3.selectAll("." + col + "rect").attr("opacity", "1");
      tooltip.style("display", "none");
    });

  //x axis
  svg.append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x))
    .append("text")
    .attr("x", width - margin.right)
    .attr("y", -10)
    .attr("fill", "#000")
    .attr("font-weight", "bold")
    .attr("text-anchor", "end")
    .text(col);

  //y axis
  svg.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y))
    .append("text")
    .attr("x", 4)
    .attr("y", 10)
    .attr("text-anchor", "start")
    .attr("font-weight", "bold")
    .attr("fill", "#000")
    .text("Count");
}



function drawRow(data, col) {
  //calculate data

  var f = d3.format("0.2~f");
  var dmax = d3.max(data, function (d) {
    return Number(d[col]);
  });
  var dmin = d3.min(data, function (d) {
    return Number(d[col]);
  });
  var dmean = d3.mean(data, function (d) {
    return Number(d[col]);
  });

  var dnul = data.filter(function (d) {
      return d[col] == "NaN";
    }),
    nul_len = dnul.length;

  var uniq_group = d3.rollup(data, v => v.length, d => d[col]);

  var uniq_cnt = 0;

  uniq_group.forEach(function (v, i) {
    //console.log(v,i);
    if (v == 1) {
      uniq_cnt++;
    };
  });

  //add block
  var block = d3.select("#ov").append("div")
    .attr("id", col + "block")
    .attr("class", "ov_block")

  // add row
  var row = d3.select("#" + col + "block").append("div")
    .attr("class", "ov_row")
    .attr("id", col);

  // add attribute name
  var attr = d3.select("#" + col).append("span")
    .attr("class", "ov_cell attr")
    .html("<b>" + col + "</b>")

  // add mini histogram

  var hg = d3.select("#" + col).append("span")
    .attr("class", "ov_cell hg")
    .attr("id", col + "hg")

  var margin = {
      top: 5,
      right: 1,
      bottom: 5,
      left: 1
    },
    width = $(".hg").width() - margin.left - margin.right,
    height = 70 - margin.top - margin.bottom;

  var map_data = data.map(function (d) {
    return Number(d[col]);
  });

  var histogram = d3.histogram()
    (map_data);

  var x = d3.scaleLinear()
    .domain(d3.extent(map_data)).nice()
    .range([margin.left, width - margin.right]);

  var histogram = d3.histogram()
    .domain(x.domain())
    .thresholds(x.ticks(60))
    (map_data);

  var y = d3.scaleLinear()
    .domain([0, d3.max(histogram, d => d.length)]).nice()
    .range([height - margin.bottom, margin.top]);

  var svg = d3.select("#" + col + "hg").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // bars
  svg.append("g")
    .attr("fill", "black")
    .selectAll("rect")
    .data(histogram)
    .enter().append("rect")
    .attr("x", d => x(d.x0) + 1)
    .attr("width", d => Math.max(0, x(d.x1) - x(d.x0)))
    .attr("y", d => y(d.length))
    .attr("height", d => y(0) - y(d.length))
    .attr("stroke", "white")
    .attr("stroke-width", "1");

  //add max
  var max = d3.select("#" + col).append("span")
    .attr("class", "ov_cell max")
    .html(f(dmax));

  //add min
  var min = d3.select("#" + col).append("span")
    .attr("class", "ov_cell min")
    .html(f(dmin));

  //add mean
  var mean = d3.select("#" + col).append("span")
    .attr("class", "ov_cell mean")
    .html(f(dmean));

  //add null entries
  var nul = d3.select("#" + col).append("span")
    .attr("class", "ov_cell nul")
    .html(f(nul_len));

  //add uniqueness
  var uniq = d3.select("#" + col).append("span")
    .attr("class", "ov_cell uniq")
    .html(f(uniq_cnt));

  //console.log("test");
  //console.log(uniq_group);
}

function toggleHis() {

  $('.ov_block').each(function () {
    var $fullhis = $(this);

    $(".ov_row", $fullhis).click(function (e) {
      e.preventDefault();
      $div = $("div.fullhis", $fullhis);
      $fullhis.toggleClass("ov_block_select");
      $(".ov_block").not($fullhis).removeClass("ov_block_select", "slow");
      $div.slideToggle();

      $("div.fullhis").not($div).hide();
      return false;
    });
  });

}