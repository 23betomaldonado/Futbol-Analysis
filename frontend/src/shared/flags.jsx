import React from "react";
export { Flag, toneOf };

const FLAG_TONE = {
  Brazil: ["#009B3A", "#FFDF00"],
  Argentina: ["#75AADB", "#F6B40E"],
  Germany: ["#000000", "#DD0000"],
};

const toneOf = (n) => FLAG_TONE[n] || ["#7A7A7A", "#D8E4E1"];

const SIMPLE_FLAGS = {
  Belgium: ["V3", "#000", "#FDDA24", "#EF3340"],
  Nigeria: ["V3", "#008751", "#fff", "#008751"],
  "Côte d'Ivoire": ["V3", "#FF8200", "#fff", "#009E60"],
  "Republic of Ireland": ["V3", "#009A49", "#fff", "#FF7900"],
  Bulgaria: ["H3", "#fff", "#00966E", "#D62612"],
  Ukraine: ["H2", "#0057B7", "#FFD700"],
  Russia: ["H3", "#fff", "#0039A6", "#D52B1E"],
  Hungary: ["H3", "#CE2939", "#fff", "#436F4D"],
  Poland: ["H2", "#fff", "#DC143C"],
};

function Flag({ nation, w = 28 }) {
  const h = Math.round(w * 0.667);
  const vb = {
    viewBox: "0 0 30 20",
    width: w,
    height: h,
    style: { display: "block", borderRadius: 2 },
  };

  const V3 = (a, b, c) => (
    <svg {...vb}>
      <rect width="10" height="20" fill={a} />
      <rect x="10" width="10" height="20" fill={b} />
      <rect x="20" width="10" height="20" fill={c} />
    </svg>
  );

  const H3 = (a, b, c) => (
    <svg {...vb}>
      <rect width="30" height="6.67" fill={a} />
      <rect y="6.67" width="30" height="6.67" fill={b} />
      <rect y="13.34" width="30" height="6.67" fill={c} />
    </svg>
  );

  const H2 = (a, b) => (
    <svg {...vb}>
      <rect width="30" height="10" fill={a} />
      <rect y="10" width="30" height="10" fill={b} />
    </svg>
  );

  const star = (cx, cy, r, fill) => (
    <polygon fill={fill} points={Array.from({ length: 10 }).map((_, i) => {
      const ang = (Math.PI / 5) * i - Math.PI / 2;
      const rad = i % 2 === 0 ? r : r * 0.42;
      return `${(cx + rad * Math.cos(ang)).toFixed(2)},${(cy + rad * Math.sin(ang)).toFixed(2)}`;
    }).join(" ")} />
  );

  switch (nation) {
    case "France": return V3("#0055A4", "#fff", "#EF4135");
    case "Italy": return V3("#008C45", "#F4F5F0", "#CD212A");
    case "Germany": case "West Germany": return H3("#000", "#DD0000", "#FFCE00");
    case "Netherlands": return H3("#AE1C28", "#fff", "#21468B");

    case "Argentina": return (
      <svg {...vb}>
        <rect width="30" height="20" fill="#75AADB" />
        <rect y="6.67" width="30" height="6.67" fill="#fff" />
        <circle cx="15" cy="10" r="2.1" fill="#F6B40E" />
      </svg>
    );
    case "Spain": return (
      <svg {...vb}>
        <rect width="30" height="5" fill="#AA151B" />
        <rect y="5" width="30" height="10" fill="#F1BF00" />
        <rect y="15" width="30" height="5" fill="#AA151B" />
        <rect x="6" y="7" width="5" height="6" fill="#AD1519" stroke="#F1BF00" strokeWidth="0.4" />
        <rect x="6" y="7" width="2.5" height="3" fill="#F1BF00" opacity="0.6" />
      </svg>
    );

    case "Brazil": return (
      <svg {...vb}>
        <rect width="30" height="20" fill="#009B3A" />
        <polygon points="15,2.5 27,10 15,17.5 3,10" fill="#FFDF00" />
        <circle cx="15" cy="10" r="4" fill="#002776" />
      </svg>
    );

    // Countries that need their real emblem, not just a color swap.
    case "Wales": return (
      <svg {...vb}>
        <rect width="30" height="10" fill="#fff" />
        <rect y="10" width="30" height="10" fill="#00B140" />
        <path d="M8,14 Q6,10 9,7 Q12,5 14,8 Q16,6 19,8 Q22,9 21,13 Q23,12 24,14 Q22,15 20,14 Q19,17 16,16 Q17,18 14,17 Q11,18 10,16 Q7,17 6,15 Q7,14 8,14 Z" fill="#C8102E" />
      </svg>
    );

    case "Slovenia": return (
      <svg {...vb}>
        {H3("#fff", "#005CE7", "#ED1C24")}
        <path d="M5,9 L8,4 L11,9 Z" fill="#005CE7" />
        <circle cx="6.3" cy="5.5" r="0.6" fill="#FFD700" />
        <circle cx="8" cy="4.7" r="0.6" fill="#FFD700" />
        <circle cx="9.7" cy="5.5" r="0.6" fill="#FFD700" />
      </svg>
    );

    case "Slovakia": return (
      <svg {...vb}>
        {H3("#fff", "#0B4EA2", "#EE1C25")}
        <rect x="5" y="5" width="6" height="8" fill="#EE1C25" stroke="#fff" strokeWidth="0.3" />
        <rect x="6.5" y="6" width="1" height="6" fill="#fff" />
        <rect x="5.5" y="8" width="4" height="1" fill="#fff" />
      </svg>
    );

    case "IR Iran": return (
      <svg {...vb}>
        {H3("#239F40", "#fff", "#DA0000")}
        <path d="M14,8.5 Q15,6.5 16,8.5 Q15,9.5 15,10.5 Q15,9.5 14,8.5Z" fill="#DA0000" />
      </svg>
    );

    case "Honduras": return (
      <svg {...vb}>
        {H3("#0073CF", "#fff", "#0073CF")}
        {[10.5, 13, 15, 17, 19.5].map((x, i) => <g key={i}>{star(x, i % 2 ? 9.5 : 10.5, 1, "#0073CF")}</g>)}
      </svg>
    );

    case "Paraguay": return (
      <svg {...vb}>
        {H3("#D52B1E", "#fff", "#0038A8")}
        <circle cx="15" cy="10" r="3" fill="none" stroke="#D52B1E" strokeWidth="0.4" />
        {star(15, 10, 1.8, "#FFD700")}
      </svg>
    );

    case "Egypt": return (
      <svg {...vb}>
        {H3("#CE1126", "#fff", "#000")}
        <path d="M15,6.5 Q13,7 12.5,9 Q13.5,8.5 14,9.5 Q13,10.5 13.5,12 Q14.5,11 15,11.5 Q15.5,11 16.5,12 Q17,10.5 16,9.5 Q16.5,8.5 17.5,9 Q17,7 15,6.5 Z" fill="#C09300" />
      </svg>
    );

        case "Romania": return (
      <svg {...vb}>
        {V3("#002B7F", "#FCD116", "#CE1126")}
        <circle cx="15" cy="10" r="2.2" fill="none" stroke="#8B4513" strokeWidth="0.5" />
        <path d="M15,8.2 Q13.5,9 13.8,10.5 Q14.5,10 15,10.8 Q15.5,10 16.2,10.5 Q16.5,9 15,8.2Z" fill="#8B4513" />
      </svg>
    );

    case "Peru": return (
      <svg {...vb}>
        {V3("#D91023", "#fff", "#D91023")}
        <rect x="13.2" y="7.5" width="3.6" height="5" fill="none" stroke="#006341" strokeWidth="0.4" />
        <circle cx="15" cy="9" r="0.8" fill="#8B4513" />
        <rect x="13.6" y="10.5" width="2.8" height="1.5" fill="#FFD700" opacity="0.7" />
      </svg>
    );

    case "Austria": return (
      <svg {...vb}>
        {H3("#ED2939", "#fff", "#ED2939")}
        <path d="M15,7.5 L13,9 L13.5,10 L11.5,9.5 L12,10.5 L14,10.8 L13,12 L15,11.3 L17,12 L16,10.8 L18,10.5 L18.5,9.5 L16.5,10 L17,9 Z" fill="#000" />
      </svg>
    );

    case "Bolivia": return (
      <svg {...vb}>
        {H3("#DA291C", "#F9E300", "#007A33")}
        <circle cx="15" cy="6.67" r="2" fill="none" stroke="#8B4513" strokeWidth="0.4" />
        <path d="M13.5,6 L16.5,6 L16,7.5 L14,7.5 Z" fill="#8B7355" />
        <circle cx="15" cy="5.3" r="0.5" fill="#FFD700" />
      </svg>
    );

    case "El Salvador": return (
      <svg {...vb}>
        {H3("#0047AB", "#fff", "#0047AB")}
        <polygon points="15,6.5 12.5,9.5 17.5,9.5" fill="none" stroke="#0047AB" strokeWidth="0.4" />
        <path d="M12.5,9.5 Q15,7.5 17.5,9.5" fill="none" stroke="#FFD700" strokeWidth="0.5" />
        <circle cx="15" cy="8" r="0.6" fill="#FFD700" />
      </svg>
    );

    case "Serbia": return (
      <svg {...vb}>
        {H3("#C6363C", "#0C4076", "#fff")}
        <rect x="6.5" y="6" width="4" height="8" fill="#C6363C" stroke="#FFD700" strokeWidth="0.3" />
        <circle cx="8.5" cy="8.5" r="1.2" fill="#FFD700" opacity="0.8" />
      </svg>
    );

    case "Yugoslavia": return (
      <svg {...vb}>
        {H3("#0039A6", "#fff", "#D52B1E")}
        <polygon fill="#D52B1E" stroke="#FFD700" strokeWidth="0.4" points={Array.from({ length: 10 }).map((_, i) => {
          const ang = (Math.PI / 5) * i - Math.PI / 2;
          const rad = i % 2 === 0 ? 2.3 : 0.95;
          return `${(15 + rad * Math.cos(ang)).toFixed(2)},${(10 + rad * Math.sin(ang)).toFixed(2)}`;
        }).join(" ")} />
      </svg>
    );

    case "Haiti": return (
      <svg {...vb}>
        {H2("#00209F", "#D21034")}
        <rect x="11.5" y="6.5" width="7" height="7" fill="#fff" />
        <path d="M15,8 L15,11.5 M13.5,8.5 Q15,7 16.5,8.5 M13,9.5 Q15,8 17,9.5" stroke="#006B3D" strokeWidth="0.5" fill="none" />
        <rect x="13.8" y="11.3" width="2.4" height="0.8" fill="#8B4513" />
      </svg>
    );

    case "Uruguay": return <svg {...vb}><rect width="30" height="20" fill="#fff" />{[0,2,4].map(k=><rect key={k} y={2.2+k*4.4} width="30" height="2.2" fill="#0038A8" />)}<rect width="13" height="11" fill="#fff" /><circle cx="6.5" cy="5.5" r="3" fill="#FCD116" /></svg>;
    case "England": return <svg {...vb}><rect width="30" height="20" fill="#fff" /><rect x="12.5" width="5" height="20" fill="#CE1124" /><rect y="7.5" width="30" height="5" fill="#CE1124" /></svg>;
    case "Switzerland": return <svg {...vb}><rect width="30" height="20" fill="#D52B1E" /><rect x="13" y="5" width="4" height="10" fill="#fff" /><rect x="10" y="8" width="10" height="4" fill="#fff" /></svg>;
    case "Sweden": return <svg {...vb}><rect width="30" height="20" fill="#006AA7" /><rect x="9" width="4" height="20" fill="#FECC02" /><rect y="8" width="30" height="4" fill="#FECC02" /></svg>;
    
    case "Chile": return <svg {...vb}><rect width="30" height="20" fill="#fff" /><rect y="10" width="30" height="10" fill="#D52B1E" /><rect width="11" height="10" fill="#0039A6" /><polygon points="5.5,2.6 6.4,5 8.9,5 6.9,6.6 7.7,9 5.5,7.5 3.3,9 4.1,6.6 2.1,5 4.6,5" fill="#fff" /></svg>;
    case "Mexico": return <svg {...vb}><rect width="10" height="20" fill="#006847" /><rect x="10" width="10" height="20" fill="#fff" /><rect x="20" width="10" height="20" fill="#CE1126" /><circle cx="15" cy="10" r="2.3" fill="#8C6239" /></svg>;
    case "United States": return <svg {...vb}><rect width="30" height="20" fill="#fff" />{[0,1,2,3,4,5,6].map(k=><rect key={k} y={k*3} width="30" height="1.5" fill="#B22234" />)}<rect width="13" height="10.5" fill="#3C3B6E" /></svg>;
    case "Korea Republic, Japan": case "Korea Republic": return <svg {...vb}><rect width="30" height="20" fill="#fff" /><path d="M15 5.5a4.5 4.5 0 0 1 0 9 4.5 4.5 0 0 0 0-9z" fill="#0047A0" /><path d="M15 5.5a4.5 4.5 0 0 0 0 9 4.5 4.5 0 0 1 0-9z" fill="#CD2E3A" /></svg>;
    
    case "South Africa": return <svg {...vb}><rect width="30" height="20" fill="#fff" /><rect y="0" width="30" height="6" fill="#DE3831" /><rect y="14" width="30" height="6" fill="#002395" /><path d="M0 0h6l10 10L6 20H0z" fill="#007A4D" /><path d="M0 3h3l9 7-9 7H0z" fill="#FFB612" /></svg>;
    case "Qatar": return <svg {...vb}><rect width="30" height="20" fill="#8A1538" /><rect width="9" height="20" fill="#fff" /><polygon points="9,0 12,2.2 9,4.4 12,6.6 9,8.8 12,11 9,13.2 12,15.4 9,17.6 12,20 9,20" fill="#fff" /></svg>;
    case "Czechoslovakia": return <svg {...vb}><rect width="30" height="10" fill="#fff" /><rect y="10" width="30" height="10" fill="#D7141A" /><polygon points="0,0 13,10 0,20" fill="#11457E" /></svg>;
    case "Croatia": return <svg {...vb}><rect width="30" height="6.67" fill="#FF0000" /><rect y="6.67" width="30" height="6.67" fill="#fff" /><rect y="13.34" width="30" height="6.67" fill="#171796" /><rect x="12" y="6" width="6" height="6" fill="#fff" stroke="#FF0000" strokeWidth="1.2" /></svg>;
    
    case "Portugal": return <svg {...vb}><rect width="12" height="20" fill="#006600" /><rect x="12" width="18" height="20" fill="#FF0000" /><circle cx="12" cy="10" r="4" fill="#FFCC00" /></svg>;
    case "Soviet Union": return <svg {...vb}><rect width="30" height="20" fill="#CC0000" />{star(7, 6, 3, "#FFD700")}</svg>;
    case "Japan": return <svg {...vb}><rect width="30" height="20" fill="#fff" /><circle cx="15" cy="10" r="5.5" fill="#BC002D" /></svg>;
    case "Denmark": return <svg {...vb}><rect width="30" height="20" fill="#C60C30" /><rect x="9" width="3.5" height="20" fill="#fff" /><rect y="8.2" width="30" height="3.5" fill="#fff" /></svg>;
    
    case "Senegal": return <svg {...vb}>{V3("#00853F", "#FDEF42", "#E31B23")}{star(15, 10, 3, "#00853F")}</svg>;
    case "Cameroon": return <svg {...vb}>{V3("#007A5E", "#CE1126", "#FCD116")}{star(15, 10, 2.6, "#FCD116")}</svg>;
    case "Saudi Arabia": return <svg {...vb}><rect width="30" height="20" fill="#006C35" /><rect x="6" y="13.5" width="18" height="2.6" fill="#fff" opacity=".85" /></svg>;
    case "Algeria": return <svg {...vb}><rect width="15" height="20" fill="#fff" /><rect x="15" width="15" height="20" fill="#006233" />{star(15, 10, 3, "#D21034")}</svg>;
    
    case "Australia": return <svg {...vb}><rect width="30" height="20" fill="#00008B" /><rect width="13" height="8" fill="#00008B" /><path d="M0,0 L13,8 M13,0 L0,8" stroke="#fff" strokeWidth="1.3" />{[[22,4],[26,12],[19,15]].map(([x,y],i)=><circle key={i} cx={x} cy={y} r="1.1" fill="#fff" />)}</svg>;
    case "Bosnia and Herzegovina": return <svg {...vb}><rect width="30" height="20" fill="#002395" /><polygon points="0,0 15,0 0,20" fill="#FECB00" />{[3,6,9,12].map(y=><circle key={y} cx={2+y*0.85} cy={y+1} r="0.9" fill="#fff" />)}</svg>;
    case "Canada": return <svg {...vb}>{V3("#FF0000", "#fff", "#FF0000")}<polygon points="15,6 16,9 19,8 17,11 19,13 16,12.5 15,15.5 14,12.5 11,13 13,11 11,8 14,9" fill="#FF0000" /></svg>;
    case "China PR": return <svg {...vb}><rect width="30" height="20" fill="#DE2910" />{star(6,5,2.6,"#FFDE00")}{[[10,2.5],[11.5,5],[10,7.5],[8,6]].map(([x,y],i)=><circle key={i} cx={x} cy={y} r=".7" fill="#FFDE00" />)}</svg>;
    
    case "Colombia": return <svg {...vb}><rect width="30" height="10" fill="#FCD116" /><rect y="10" width="30" height="5" fill="#003893" /><rect y="15" width="30" height="5" fill="#CE1126" /></svg>;
    case "Costa Rica": return <svg {...vb}><rect width="30" height="20" fill="#002B7F" /><rect y="3.3" width="30" height="13.4" fill="#fff" /><rect y="6.7" width="30" height="6.6" fill="#CE1126" /></svg>;
    case "Cuba": return <svg {...vb}>{[0,1,2,3,4].map(i=><rect key={i} y={i*4} width="30" height="4" fill={i%2?"#fff":"#002A8F"} />)}<polygon points="0,0 10,10 0,20" fill="#CF142B" />{star(4,10,2.2,"#fff")}</svg>;
    case "Czech Republic": return <svg {...vb}><rect width="30" height="10" fill="#fff" /><rect y="10" width="30" height="10" fill="#D7141A" /><polygon points="0,0 13,10 0,20" fill="#11457E" /></svg>;
    
    case "Ecuador": return <svg {...vb}><rect width="30" height="10" fill="#FFDD00" /><rect y="10" width="30" height="5" fill="#034EA2" /><rect y="15" width="30" height="5" fill="#ED1C24" /></svg>;
    case "FR Yugoslavia": case "Serbia and Montenegro": case "Germany DR":
    case "Dutch East Indies": case "Zaire": case "Angola": {
    
      const [a2, b2] = toneOf(nation); return <svg {...vb}><rect width="30" height="20" fill={a2} /><rect y="13" width="30" height="7" fill={b2} /></svg>;
    }
    case "Ghana": return <svg {...vb}>{H3("#CE1126", "#FCD116", "#006B3F")}{star(15, 6.7, 2.2, "#000")}</svg>;
    case "Greece": return <svg {...vb}><rect width="30" height="20" fill="#0D5EAF" />{[0,2,4,6,8].map(y=><rect key={y} y={y*2} width="30" height="2" fill="#fff" />)}<rect width="8" height="11" fill="#0D5EAF" /><rect x="3" width="2" height="11" fill="#fff" /><rect y="4.5" width="8" height="2" fill="#fff" /></svg>;
    case "Iceland": return <svg {...vb}><rect width="30" height="20" fill="#02529C" /><rect x="10" width="4" height="20" fill="#fff" /><rect y="8" width="30" height="4" fill="#fff" /><rect x="11.2" width="1.6" height="20" fill="#DC1E35" /><rect y="9.2" width="30" height="1.6" fill="#DC1E35" /></svg>;
    case "Iraq": return <svg {...vb}>{H3("#CE1126", "#fff", "#000")}{star(15,10,1.6,"#007A3D")}</svg>;
    
    case "Israel": return <svg {...vb}><rect width="30" height="20" fill="#fff" /><rect y="2.5" width="30" height="2.8" fill="#0038B8" /><rect y="14.7" width="30" height="2.8" fill="#0038B8" />{star(15,10,3.6,"#0038B8")}</svg>;
    case "Jamaica": return <svg {...vb}><polygon points="0,0 15,10 0,20" fill="#009B3A" /><polygon points="30,0 15,10 30,20" fill="#009B3A" /><polygon points="0,0 15,10 30,0" fill="#000" /><polygon points="0,20 15,10 30,20" fill="#000" /><polygon points="12,10 15,8.5 18,10 15,11.5" fill="#FED100" /></svg>;
    case "Korea DPR": return <svg {...vb}><rect width="30" height="20" fill="#fff" /><rect y="3" width="30" height="14" fill="#024FA2" /><rect y="8.6" width="30" height="2.8" fill="#fff" /><rect y="9.3" width="30" height="1.4" fill="#ED1C27" /><circle cx="7" cy="10" r="2.6" fill="#ED1C27" />{star(7,10,1.1,"#fff")}</svg>;
    case "Kuwait": return <svg {...vb}>{H3("#007A3D", "#fff", "#CE1126")}<polygon points="0,0 6,0 0,10" fill="#000" /><polygon points="0,20 6,20 0,10" fill="#000" /></svg>;
    
    case "Morocco": return <svg {...vb}><rect width="30" height="20" fill="#C1272D" />{star(15,10,3.4,"#006233")}</svg>;
    case "New Zealand": return <svg {...vb}><rect width="30" height="20" fill="#00247D" /><rect width="13" height="8" fill="#00247D" /><path d="M0,0 L13,8 M13,0 L0,8" stroke="#fff" strokeWidth="1.2" />{[[22,5],[25,10],[21,14],[24,3]].map(([x,y],i)=><g key={i}>{star(x,y,1.4,"#fff")}</g>)}</svg>;
    case "Northern Ireland": return <svg {...vb}><rect width="30" height="20" fill="#fff" /><rect x="13" width="4" height="20" fill="#CE1124" /><rect y="8" width="30" height="4" fill="#CE1124" />{star(15,10,2.4,"#CE1124")}</svg>;
    case "Norway": return <svg {...vb}><rect width="30" height="20" fill="#EF2B2D" /><rect x="10" width="4" height="20" fill="#fff" /><rect y="8" width="30" height="4" fill="#fff" /><rect x="11.2" width="1.6" height="20" fill="#002868" /><rect y="9.2" width="30" height="1.6" fill="#002868" /></svg>;
    
    case "Panama": return <svg {...vb}><rect width="15" height="10" fill="#fff" /><rect x="15" width="15" height="10" fill="#DA121A" /><rect y="10" width="15" height="10" fill="#0072C6" /><rect x="15" y="10" width="15" height="10" fill="#fff" />{star(7.5,5,1.8,"#0072C6")}{star(22.5,15,1.8,"#DA121A")}</svg>;
    case "Scotland": return <svg {...vb}><rect width="30" height="20" fill="#005EB8" /><path d="M0,0 L30,20 M30,0 L0,20" stroke="#fff" strokeWidth="3" /></svg>;
    case "Togo": return <svg {...vb}>{[0,1,2,3,4].map(i=><rect key={i} y={i*4} width="30" height="4" fill={i%2?"#FFCE00":"#006A4E"} />)}<rect width="9" height="12" fill="#D21034" />{star(4.5,6,2,"#fff")}</svg>;
    case "Trinidad and Tobago": return <svg {...vb}><rect width="30" height="20" fill="#CE1126" /><polygon points="0,0 7,0 27,20 20,20" fill="#fff" /><polygon points="0,4 4,0 30,16 30,20" fill="#000" /></svg>;
    
    case "Tunisia": return <svg {...vb}><rect width="30" height="20" fill="#E70013" /><circle cx="15" cy="10" r="5.5" fill="#fff" />{star(15,10,2.2,"#E70013")}</svg>;
    case "Türkiye": return <svg {...vb}><rect width="30" height="20" fill="#E30A17" /><circle cx="12" cy="10" r="4.4" fill="#fff" /><circle cx="13.3" cy="10" r="3.6" fill="#E30A17" />{star(17,10,1.8,"#fff")}</svg>;
    case "United Arab Emirates": return <svg {...vb}><rect x="6" width="24" height="6.67" fill="#00732F" /><rect x="6" y="6.67" width="24" height="6.67" fill="#fff" /><rect x="6" y="13.34" width="24" height="6.67" fill="#000" /><rect width="6" height="20" fill="#FF0000" /></svg>;

    default: {
      // Simple flags = flags that have similar shapes, but different colors.
      // Prevents repetition and simplifies to just a change in color.
      if (SIMPLE_FLAGS[nation]) {
        const [type, ...colors] = SIMPLE_FLAGS[nation];
        if (type === "V3") return V3(...colors);
        if (type === "H3") return H3(...colors);
        return H2(...colors);
      }
      const [a, b] = toneOf(nation);
      return (
        <svg {...vb}>
          <rect width="30" height="20" fill={a} />
          <rect y="13" width="30" height="7" fill={b} />
        </svg>
      );
    }
  }
}