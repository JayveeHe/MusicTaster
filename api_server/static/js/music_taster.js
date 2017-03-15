/**
 * Created by jayvee on 17/3/15.
 * https://github.com/JayveeHe
 */


// 歌单聚类
$("#btn_send").click(function () {
    var pl_url = $("#input_url").val();
    var send_datas = {
        url: pl_url,
        type: "song"
    };
    $.ajax('/cluster/playlist/url', {
        'data': JSON.stringify(send_datas), //{action:'x',params:['a','b','c']}
        'type': 'POST',
        'processData': false,
        'contentType': 'application/json' //typically 'application/x-www-form-urlencoded', but the service you are calling may expect 'text/json'... check with the service to see what they expect as content-type in the HTTP header.
    }).done(function (data, status) {
            $("#show_cluster").modal('toggle');
            if (status == "success") {
                // parse cluster result
                //解析聚类结果
                var resp_obj = eval(data);
                if (resp_obj['code'] == 200) {
                    var title = $("#playlist_name_title");
                    console.log(resp_obj['playlist_name']);
                    title.val(resp_obj['playlist_name'] + "\t" + title.val());
                    /// -------- d3.js -------
                    //准备复杂网络数据
                    var g = {"nodes": [], "links": []};
                    var cluster_result = resp_obj["result"];
                    g.nodes.push({'id': 'root', 'group': -1, 'label': 'root'});
                    for (var i = 0; i < cluster_result.length; i++) {
                        console.log(cluster_result[i]);
                        var item = cluster_result[i][0];
                        /**var c_color = '#' + (Math.floor(Math.random() * 16777215).toString(16) + '000000').substr(0, 6);
                         var c_x = (Math.random() - 0.5) * 50;
                         var c_y = (Math.random() - 0.5) * 50;**/
                        g.nodes.push({
                            "id": item,
                            "group": i,
                            'label': item
                        });
                        g.links.push({
                            'source': 'root',
                            'target': item,
                            'value': 1
                        });
                        var c_root_id = item;
                        var last_item = c_root_id;
                        for (var j = 1; j < cluster_result[i].length; j++) {
                            //console.log(i + "-" + j);
                            var n_item = cluster_result[i][j];
                            g.nodes.push({
                                "id": n_item,
                                "group": i,
                                'label': n_item
                            });
                            g.links.push({
                                'value': 1,
                                'source': c_root_id,
                                'target': n_item
                            });
                        }
                    }

                    // d3 初始化
                    var svg = d3.select("svg");

                    svg.selectAll('*').remove();
                    var c_canvas = $('#cluster_canvas');
                    var svg_width = 1000 * 0.9;
                    var svg_height = 500 * 0.9;
                    //console.log(c_canvas.parentElement().width + '-' + c_canvas.parentElement().height);
                    console.log('svg_width:' + svg_width + '\theight:' + svg_height);

                    var color = d3.scaleOrdinal(d3.schemeCategory20);

                    var simulation = d3.forceSimulation()
                        .force("link", d3.forceLink().id(function (d) {
                            return d.id;
                        }))
                        .force("charge", d3.forceManyBody())
                        .force("center", d3.forceCenter(svg_width / 2, svg_height / 2));


                    var link = svg.append("g")
                        .attr("class", "links")
                        .selectAll("line")
                        .data(g.links)
                        .enter().append("line")
                        .attr("stroke-width", function (d) {
                            return Math.sqrt(d.value);
                        });

                    var node = svg.append("g")
                        .attr("class", "nodes")
                        .selectAll("circle")
                        .data(g.nodes)
                        .enter()
                        .append("circle")
                        .attr("r", 5)
                        .attr("fill", function (d) {
                            return color(d.group);
                        })
                        .call(d3.drag()
                            .on("start", dragstarted)
                            .on("drag", dragged)
                            .on("end", dragended));

                    var anchorNode = svg.append('g').attr('class', 'labels').selectAll("g.labels").data(g.nodes)
                        .enter().append("svg:text").text(function (d) {
                            return d.label;
                        }).style("fill", "#555").style("font-family", "Arial").style("font-size", 6)
                        .call(d3.drag()
                            .on("start", dragstarted)
                            .on("drag", dragged)
                            .on("end", dragended));
                    //anchorNode.append("svg:circle").attr("r", 0).style("fill", "#FFF");


                    simulation
                        .nodes(g.nodes)
                        .on("tick", ticked);

                    simulation.force("link")
                        .links(g.links);
                    var zoom = d3.zoom()
                        .on("zoom", zoomed);

                    svg
                        .on("wheel", wheeled)
                        .call(zoom)
                        .call(zoom.transform, d3.zoomIdentity
                            .translate(svg_width / 2, svg_height / 2)
                            .scale(0.5)
                            .translate(-svg_width / 2, -svg_height / 2));
                    svg.call(zoom);

                    function wheeled() {
                        console.log(d3.event);
                    }

                    function zoomed() {
                        node.attr("transform", d3.event.transform);
                        link.attr("transform", d3.event.transform);
                        anchorNode.attr("transform", d3.event.transform);
                    }

                    function ticked() {
                        link
                            .attr("x1", function (d) {
                                return d.source.x;
                            })
                            .attr("y1", function (d) {
                                return d.source.y;
                            })
                            .attr("x2", function (d) {
                                return d.target.x;
                            })
                            .attr("y2", function (d) {
                                return d.target.y;
                            });

                        node
                            .attr("cx", function (d) {
                                return d.x;
                            })
                            .attr("cy", function (d) {
                                return d.y;
                            });
                        anchorNode
                            .attr("x", function (d) {
                                return d.x;
                            })
                            .attr("y", function (d) {
                                return d.y;
                            });
                    }

                    function dragstarted(d) {
                        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
                        d.fx = d.x;
                        d.fy = d.y;
                    }

                    function dragged(d) {
                        d.fx = d3.event.x;
                        d.fy = d3.event.y;
                    }

                    function dragended(d) {
                        if (!d3.event.active) simulation.alphaTarget(0);
                        d.fx = null;
                        d.fy = null;
                    }


                }
                else {
                    alert("请求错误,详情=" + resp_obj.toString());
                }
            }
            else {
                alert("请求失败");
            }
        }
    ).fail(function () {
        alert("请求失败");
    });
});




