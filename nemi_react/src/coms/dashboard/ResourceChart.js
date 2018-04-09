let ResourceOption = (data, data_list) => {return {
    backgroundColor: 'rgb(43, 51, 59)',
    toolbox: {
        show: true,
        feature: {
            mark: {
                show: true
            },
            dataView: {
                show: true,
                readOnly: false
            },
            magicType: {
                show: true,
                type: ['pie', 'funnel']
            },
            restore: {
                show: true
            },
            saveAsImage: {
                show: true
            }
        }
    },
    calculable: true,
    tooltip: {
        trigger: "item",
        formatter: "{a}<br/>{b}:{c}个"
    },
    title: {
        text: "",
        left: "center",
        top: 20,
        textStyle: {
            "color": "#ccc"
        }
    },
    legend: {
        icon: "circle",
        x: 'center',
        y: 'bottom',
        data: data_list,
        textStyle: {
            "color": "#fff"
        }
    },
    series: [{
        name: "文件类型",
        type: "pie",
        radius: [
            37,
            155
        ],
        avoidLabelOverlap: true,
        startAngle: 0,
        center: [
            "60%",
            "20%"
        ],
        roseType: "area",
        selectedMode: "single",
        label: {
            normal: {
                show: false,
                formatter: "{c}个"
            },
            emphasis: {
                show: false
            }
        },
        labelLine: {
            normal: {
                show: false,
                smooth: false,
                length: 20,
                length2: 10
            },
            emphasis: {
                show: false
            }
        },
        data: data
    }]
};}

export {ResourceOption};