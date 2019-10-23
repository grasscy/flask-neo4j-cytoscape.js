document.addEventListener('DOMContentLoaded', function () {
    axios.defaults.headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8"
    };
    axios.defaults.baseURL = 'http://127.0.0.1:5000'

    axios.interceptors.request.use(
        config => {
            if (!app.label) {
                app.dialogLabelVisible = true
            }
            console.log(app.label)
            config.headers['Label'] = app.label;
            return config;
        }, function (error) {
            return Promise.reject(error);
        })

    function click_action(node) {
        app.name = node.data('name')
        app.brief = node.data('brief')
        app.content = node.data('content')
        if (app.source_id) {
            axios({
                method: 'post',
                url: '/graph/relations?source_id=' + app.source_id + '&target_id=' + node.id(),
            }).then(function (response) {
                cy.add({
                    group: 'edges', data: {source: app.source_id, target: node.id(), relationship: ''}
                })
                app.source_id = ''
                node.unselect()
                console.log(response.data)
            }).catch(function (error) {
                console.log(error)
            });
        }
    }

    function init_mouse(node) {
        let t = makeTippy(node, node.data().brief)
        node.on('mouseover', function (e) {
            t.show();
        })
        node.on('mouseout', function (e) {
            t.hide();
        })
    }

    function makeTippy(node, text) {
        return tippy(node.popperRef(), {
            content: function () {
                var div = document.createElement('div');
                div.innerHTML = text;
                return div;
            },
            trigger: 'manual',
            arrow: true,
            placement: 'bottom',
            hideOnClick: false,
            multiple: true,
            sticky: true,
        });

    }

    function get_graph() {
        axios.get('/graph/')
            .then(function (response) {
                console.log(response.data.elements)
                let cy = window.cy = cytoscape({
                    container: document.getElementById('cy'),
                    style: [
                        {
                            selector: 'node',
                            css: {'background-color': '#6FB1FC', 'content': 'data(name)'}
                        },
                        {
                            selector: 'edge',
                            css: {'content': 'data(relationship)', 'target-arrow-shape': 'triangle'}
                        },
                        {
                            selector: "node:selected",
                            style: {
                                "border-width": "6px",
                                "border-color": "#AAD8FF",
                                "border-opacity": "0.5",
                                "background-color": "#77828C",
                                "text-outline-color": "#77828C"
                            }
                        }
                    ],
                    elements: response.data.elements,
                    layout: {name: 'cose'}
                });

                cy.nodes().on('click', function (e) {
                    click_action(e.target);
                });


                cy.nodes().forEach(function (node) {
                    init_mouse(node);
                });


                cy.cxtmenu({
                    selector: 'node',
                    commands: [
                        {
                            content: '删除',
                            select: function (ele) {
                                axios({
                                    method: 'delete',
                                    url: '/graph/concepts/' + ele.id(),
                                }).then(function (response) {
                                    cy.remove(ele)
                                }).catch(function (error) {
                                    console.log(error)
                                });
                            }
                        },
                        {
                            content: '关系到',
                            select: function (ele) {
                                app.source_id = ele.id()
                                ele.select()
                            },
                        },
                        {
                            content: '添加',
                            select: function (ele) {
                                window.oncontextmenu = function (e) {
                                    e.preventDefault();
                                }
                                app.source_id = ele.id()
                                app.dialogAddVisible = true
                            },
                        },
                        {
                            content: '修改',
                            select: function (ele) {
                                window.oncontextmenu = function (e) {
                                    e.preventDefault();
                                }
                                app.id = ele.id()
                                app.form.name = ele.data().name
                                app.form.brief = ele.data().brief
                                app.form.content = ele.data().content
                                app.dialogUpdateVisible = true
                            }
                        }
                    ],
                    menuRadius: 70,
                    activePadding: 10, // additional size in pixels for the active command
                })

                cy.cxtmenu({
                    selector: 'core',
                    commands: [
                        {
                            content: '<span class="fa fa-star fa-2x"></span>',
                            // select: function () {
                            //     console.log('bg1');
                            // },
                            enabled: false
                        },
                        {
                            content: '添加',
                            select: function () {
                                window.oncontextmenu = function (e) {
                                    //取消默认的浏览器自带右键 很重要！！
                                    e.preventDefault();
                                }
                                app.dialogAddVisible = true
                            },
                        },

                    ],
                    menuRadius: 30,
                    activePadding: 5, // additional size in pixels for the active command
                    indicatorSize: 0, // the size in pixels of the pointer to the active command
                    separatorWidth: 2, // the empty spacing in pixels between successive commands
                    spotlightPadding: 4, // extra spacing in pixels between the element and the spotlight
                    minSpotlightRadius: 2, // the minimum radius in pixels of the spotlight
                    maxSpotlightRadius: 30, // the maximum radius in pixels of the spotlight
                })

                cy.cxtmenu({
                    selector: 'edge',
                    commands: [
                        {
                            content: '删除',
                            select: function (ele) {
                                axios({
                                    method: 'delete',
                                    url: '/graph/relations?source_id=' + ele.source().id() + '&target_id=' + ele.target().id(),
                                }).then(function (response) {
                                    cy.remove(ele)
                                }).catch(function (error) {
                                    console.log(error)
                                });
                            },
                        },
                        {
                            content: '<span class="fa fa-star fa-2x"></span>',
                            enabled: false
                        },

                    ],
                    menuRadius: 30,
                    activePadding: 5, // additional size in pixels for the active command
                    indicatorSize: 0, // the size in pixels of the pointer to the active command
                    separatorWidth: 2, // the empty spacing in pixels between successive commands
                    spotlightPadding: 4, // extra spacing in pixels between the element and the spotlight
                    minSpotlightRadius: 2, // the minimum radius in pixels of the spotlight
                    maxSpotlightRadius: 30, // the maximum radius in pixels of the spotlight
                })


            })
            .catch(function (error) {
                console.log(error)
            });
    }

    let app = new Vue({
        el: '#concept',
        data: {
            id: '',
            name: '',
            brief: '',
            content: '',
            source_id: '',
            target_id: '',
            label: '',
            dialogAddVisible: false,
            dialogUpdateVisible: false,
            dialogLabelVisible: false,
            form: {
                name: '',
                brief: '',
                content: ''
            },
            formLabelWidth: '120px'
        },
        methods: {
            add_concept() {
                this.dialogAddVisible = false
                axios({
                    method: 'post',
                    url: '/graph/concepts',
                    headers: {'Content-Type': 'application/json'},
                    data: {
                        source_id: this.source_id,
                        name: this.form.name,
                        brief: this.form.brief,
                        content: this.form.content
                    }
                }).then(function (response) {
                    console.log(response.data.data)
                    cy.add({
                        group: 'nodes',
                        data: response.data.data
                    })
                    n = cy.getElementById(response.data.data.id)
                    n.on('click', function (e) {
                        click_action(e.target);
                    });
                    init_mouse(n)
                }).catch(function (error) {
                    console.log(error)
                });
            },
            update_concept() {
                this.dialogUpdateVisible = false
                axios({
                    method: 'put',
                    url: '/graph/concepts/' + this.id,
                    headers: {'Content-Type': 'application/json'},
                    data: {
                        name: this.form.name,
                        brief: this.form.brief,
                        content: this.form.content
                    }
                }).then(function (response) {
                    d = response.data.data
                    n = cy.getElementById(d.id)
                    n.data({
                        name: d.name,
                        brief: d.brief,
                        content: d.content
                    })
                    n.removeListener('mouseover');
                    init_mouse(n)
                }).catch(function (error) {
                    console.log(error)
                });
            },
            update_label() {
                this.dialogLabelVisible = false
                get_graph()
            }
        }
    })


    app.dialogLabelVisible = true

})