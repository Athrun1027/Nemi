let SpaceOption = (data) => {return {
    tooltip: {
        formatter: "{a} <br/>{b} : {c}%"
    },
    series: [{
        name: '指标',
        type: 'gauge',
        axisLine: {
            show: true,
            lineStyle: {
                width: 20,
                shadowBlur: 0,
                color: [
                    [0.2, '#90ee90'],
                    [0.4, '#ffa500'],
                    [0.6, '#87ceeb'],
                    [0.8, '#87ceeb'],
                    [1, '#ff4500']
                ]
            }
        },
        axisLabel: {
            formatter: function(e) {
                switch (e + "") {
                    case "0":
                        return "0%";
                    case "20":
                        return "20%";
                    case "40":
                        return "40%";
                    case "60":
                        return "60%";
                    case "80":
                        return "80%";
                    case "100":
                        return "100%";
                    default:
                        return "";
                }
            },
            textStyle: {
                fontSize: 15,
                fontWeight: ""
            }
        },
        startAngle: 140,
        endAngle: -140,
        axisTick: {
            splitNumber: 5
        },
        detail: {
            formatter: '{value}%',
            textStyle: {
                fontSize: 2,
                fontWeight: ""
            }
        },
        data: [{
            value: data,
            name: ''
        }]
    }]
};}
export {SpaceOption};