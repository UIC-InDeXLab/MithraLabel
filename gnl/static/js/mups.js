var uniqueColumns = {};
var color = d3v3.scale.category20();
var column = 1;

$(document).ready(function () {
	//
});

// function trying(){
// 	  $.ajax(
// 	{
// 	  type : 'GET',
// 	  url : "/api/coverage/",
// 	  contentType: "application/json;charset=UTF-8",
// 	  dataType:'json',
// 	  success : function(data)
// 	  {
// 			console.log("received data ajax");
//
// 	    loadJson("mups.json")
//
// 	  }/*success : function() {}*/
// 	});/*$.ajax*/
// }

function load_mups() {
	var today = new Date();
	$.ajax({
		type: 'GET',
		url: "/api/coverage/",
		contentType: "application/json;charset=UTF-8",
		dataType: 'json',
		success: function (dat) {
			// console.log("mups ajax back", today.getMinutes() + ":" + today.getSeconds() + ":" + today.getMilliseconds());
			// console.log("mups ", dat.tree);
			drawTree(dat.tree);
		}
	});
}

function loadJson(fileName) {
	console.log("mups here");
	d3v3.json("/static/data/" + fileName, function (error, data) {
		// console.log("data");
		// console.log(data);
		drawTree(data);
	});
}

function drawTree(data) {
	var margin = {
			top: 20,
			right: 120,
			bottom: 20,
			left: 120
		},
		width = 1200 - margin.right - margin.left,
		height = 1200 - margin.top - margin.bottom;

	/*  var margin = {top: 80, right: 0, bottom: 10, left: 80},
	      width = 600,
	      height = 600;*/

	var i = 0,
		duration = 750,
		root;

	var tree = d3v3.layout.tree()
		.size([height, width]);

	var diagonal = d3v3.svg.diagonal()
		.projection(function (d) {
			return [d.y, d.x];
		});

	var svg = d3v3.select("#mups_vis").append("svg")
		.attr("width", width + margin.right + margin.left)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
	//console.log("-------");
	//console.log(data);

	root = data[0];
	root.x0 = height / 2;
	root.y0 = 0;

	update(root);

	d3v3.select(self.frameElement).style("height", "500px");

	function update(source) {

		// Compute the new tree layout.
		var nodes = tree.nodes(root).reverse(),
			links = tree.links(nodes);
		//console.log(nodes);
		//console.log(links);

		// Normalize for fixed-depth.
		nodes.forEach(function (d) {
			d.y = d.depth * 180;
		});

		// Update the nodes…
		var node = svg.selectAll("g.node")
			.data(nodes, function (d) {
				return d.id || (d.id = ++i);
			});

		// Enter any new nodes at the parent's previous position.
		var nodeEnter = node.enter().append("g")
			.attr("class", "node")
			.attr("transform", function (d) {
				return "translate(" + source.y0 + "," + source.x0 + ")";
			})
			.on("click", click);

		nodeEnter.append("circle")
			.attr("r", 1e-6)
			.style("fill", function (d) {
				return d._children ? "lightsteelblue" : "#fff";
			})
			.style("stroke", function (d) {
				val = d.node.split(":");
				if (val[0] in uniqueColumns) {
					return uniqueColumns[val[0]];
				} else {
					uniqueColumns[val[0]] = color(column);
					column++;
					return uniqueColumns[val[0]]
				}
			});

		nodeEnter.append("text")
			.attr("x", function (d) {
				return d.children || d._children ? -13 : 13;
			})
			.attr("dy", ".35em")
			.attr("text-anchor", function (d) {
				return d.children || d._children ? "end" : "start";
			})
			.text(function (d) {
				val = d.node.split(":");
				if (val[1] != undefined) {
					return val[0] + ": " + val[1];
				} else {
					return val[0];
				}
			})
			.style("fill-opacity", 1e-6);

		// Transition nodes to their new position.
		var nodeUpdate = node.transition()
			.duration(duration)
			.attr("transform", function (d) {
				return "translate(" + d.y + "," + d.x + ")";
			});

		nodeUpdate.select("circle")
			.attr("r", 10)
			.style("fill", function (d) {
				val = d.node.split(":");
				return d._children ? uniqueColumns[val[0]] : "#fff";
			});

		nodeUpdate.select("text")
			.style("fill-opacity", 1);

		// Transition exiting nodes to the parent's new position.
		var nodeExit = node.exit().transition()
			.duration(duration)
			.attr("transform", function (d) {
				return "translate(" + source.y + "," + source.x + ")";
			})
			.remove();

		nodeExit.select("circle")
			.attr("r", 1e-6);

		nodeExit.select("text")
			.style("fill-opacity", 1e-6);

		// Update the links…
		var link = svg.selectAll("path.link")
			.data(links, function (d) {
				return d.target.id;
			});

		// Enter any new links at the parent's previous position.
		link.enter().insert("path", "g")
			.attr("class", "link")
			.attr("d", function (d) {
				var o = {
					x: source.x0,
					y: source.y0
				};
				return diagonal({
					source: o,
					target: o
				});
			});

		// Transition links to their new position.
		link.transition()
			.duration(duration)
			.attr("d", diagonal);

		// Transition exiting nodes to the parent's new position.
		link.exit().transition()
			.duration(duration)
			.attr("d", function (d) {
				var o = {
					x: source.x,
					y: source.y
				};
				return diagonal({
					source: o,
					target: o
				});
			})
			.remove();

		// Stash the old positions for transition.
		nodes.forEach(function (d) {
			d.x0 = d.x;
			d.y0 = d.y;
		});
	}

	// Toggle children on click.
	function click(d) {
		if (d.children) {
			d._children = d.children;
			d.children = null;
		} else {
			d.children = d._children;
			d._children = null;
		}
		update(d);
	}
}