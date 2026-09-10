import React from "react";

const FLAG_TONE = {
    Brazil: ["#009B3A", "#FFDF00"],
    Argentina: ["#75AADB", "#F6B40E"],
    Germany: ["#000000", "#DD0000"],
};

const toneOf = (n) => FLAG_TONE[n] || ["#7A7A7A", "#D8E4E1"];

function Flag({nation, w = 28}) {
    const h = Math.round(w * 0.667);
    const vb = {
        viewBox: "0 0 30 20", 
        width: w, 
        height: h, 
        style: {display: "block", borderRadius: 2}};

    const V3 = (a, b, c) => (
        <svg {...vb}>
            <rect width = "10" height = "20" fill = {a} />
            <rect x = "10" width = "10" height = "20" fill = {b} />
            <rect x = "20" width = "10" height = "20"  fill = {c} />
        </svg>
    );

    const H3 = (a, b, c) => (
        <svg {...vb}>
            <rect width = "30" height = "6.67" fill = {a} />
            <rect y = "6.67" width = "30" height = "6.67" fill = {b} />
            <rect y = "13.34" width = "30" height = "6.67"  fill = {c} />
        </svg>
    );

    const H2 = (a, b) => <svg {...vb}><rect width = "30" height = "10" fill = {a} /><rect y = "10" width = "30" height = "10" fill = {b} /> </svg>;

    const star = (cx, cy, r, fill) => (
        <polygon fill ={fill} points ={Array.from({ length: 10}).map((_, i) =>{
            const ang =(Math.PI / 5) * i - Math.PI / 2;
            const rad = i % 2 == 0 ? r : r * 0.42;
            return `${(cx + rad * Math.cos(ang)).toFixed(2)}, ${(cy + rad * 
            Math.sin(ang)).toFixed(2)}`;    
            }).join (" ")} />
    );

    switch(nation){
        case "France": return V3("#0055A4","#fff","#EF4135");
        case "Italy": return V3("#008C45","#F4F5F0","#CD212A");
        case "Germany": case "West Germany": return H3("#000","#DD0000","#FFCE00");
        case "Netherlands": return H3("#AE1C28","#fff","#21468B");
        case "Argentina": return (
            <svg {... vb}>
                <rect width = "30" height = "20" fill = "#75AADB"/>
                <rect y = "6.67" width = "30" height = "6.67" fill = "#fff"/>
                <circle cx = "15" cy ="10" r = "2.1" fill = "#F6B40E"/>
            </svg>
        );
        case "Brazil": return (
            <svg {... vb}>
                <rect width = "30" height = "20" fill = "#009B3A"/>
                <polygon points = "15, 2.5, 27, 10 15, 17.5 3, 10" fill = "#FFDF00"/>
                <circle cx = "15" cy ="10" r = "4" fill = "#002776" />
            </svg>
        );


        default: {
            const [a, b] = toneOf(nation);
            return (
                <svg {...vb}>
                    <rect width ="30" height="20" fill = {a} />
                    <rect y ="13" width ="30" height = "7" fill = {b} />
                </svg>
            );
        }
    }
}