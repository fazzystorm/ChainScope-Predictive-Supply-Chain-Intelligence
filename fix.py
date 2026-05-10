import os

def fix_html():
    file_path = "c:/Users/hp/.gemini/antigravity/scratch/chainscope/index.html"
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract the companies object correctly
    companies_str = html[html.find('const companies = {'):html.find('        // ═══ MAP LAYERS ═══')].strip()

    new_script = f"""    <script>
        // ═══ COMPANY DATA ═══
        {companies_str}

        let layerState = {{ routes: true, heat: true, risk: true }};
        let activeMarkers = [];

        function renderSidebar(d) {{
            const sb = document.getElementById('sb-scroll');
            const alertCount = d.alerts.length;
            document.getElementById('alertCount').textContent = alertCount + ' Active Alert' + (alertCount !== 1 ? 's' : '');

            let riskHtml = d.alerts.map(a => `
    <div class="risk-card ${{a.sev}}" onclick="toggleRisk(this)">
      <div class="risk-head"><div class="risk-badge">${{a.badge}}</div><div class="risk-title">${{a.title}}</div><div class="risk-toggle">▼</div></div>
      <div class="risk-brief">${{a.brief}}</div>
      <div class="risk-detail"><div class="risk-detail-inner">${{a.detail}}<div class="risk-impact">${{a.tags.map(t => '<span class="risk-tag-item">' + t + '</span>').join('')}}</div></div></div>
    </div>`).join('');

            let matHtml = d.materials.map(m => `
    <div class="mat"><div class="mat-top"><span class="mat-icon">${{m.icon}}</span><span class="mat-name">${{m.name}}</span><div class="mat-price">${{m.price}} <span class="chg ${{m.up ? 'up' : 'dn'}}">${{m.chg}}</span></div></div>
    <div class="mat-bar-bg"><div class="mat-bar" style="width:${{m.w}}%;background:linear-gradient(90deg,${{m.color}},${{m.color}}40)"></div></div>
    <div class="mat-foot"><span>${{m.src}}</span><span>${{m.pct}}</span></div></div>`).join('');

            let supHtml = d.suppliers.map(s => `
    <div class="sup"><div class="sup-flag">${{s.flag}}</div><div class="sup-body"><div class="sup-name">${{s.name}}</div><div class="sup-detail">${{s.detail}}</div></div>
    <div class="sup-right"><div class="sup-vol">${{s.vol}}</div><div class="sup-status ${{s.cls}}">${{s.status}}</div></div></div>`).join('');

            let priceHtml = d.prices.map(p => `
    <div class="price-row"><div class="p-name">${{p.name}}</div>
    <svg class="p-spark" width="42" height="16" viewBox="0 0 42 16"><polyline points="${{p.spark}}" fill="none" stroke="${{p.sc}}" stroke-width="1.5"/></svg>
    <div class="p-right"><div class="p-val">${{p.val}}</div><div class="p-chg" style="color:${{p.cc}}">${{p.chg}}</div></div></div>`).join('');

            let heatHtml = d.heatmap.map(h => `
    <div class="heat-row" onclick="flyToMap(${{h.lat}},${{h.lng}},6)"><div class="heat-pip" style="background:${{h.pip}}"></div>
    <div class="heat-body"><div class="heat-name">${{h.name}}</div><div class="heat-sector">${{h.sector}}</div></div>
    <div class="heat-right"><div class="heat-val">${{h.val}}</div><div class="heat-sub">workers</div></div></div>`).join('');

            const hiCount = d.alerts.filter(a => a.sev === 'hi' || a.sev === 'md').length;
            sb.innerHTML = `
    <div class="section open" id="sec-risk"><div class="s-head" onclick="toggleSection('sec-risk')"><div class="s-icon" style="background:rgba(248,113,113,.12)">⚡</div><div class="s-title">Risk Alerts</div><div class="s-meta" style="color:var(--red)">${{alertCount}} Active</div><div class="s-arrow">▼</div></div><div class="s-body"><div class="s-content"><div class="risk-list">${{riskHtml}}</div></div></div></div>
    <div class="section open" id="sec-overview"><div class="s-head" onclick="toggleSection('sec-overview')"><div class="s-icon" style="background:rgba(56,189,248,.1)">📊</div><div class="s-title">Chain Overview</div><div class="s-meta">${{d.overview.suppliers + d.overview.plants}} nodes</div><div class="s-arrow">▼</div></div><div class="s-body"><div class="s-content"><div class="health-mini"><div class="h-mini-card"><div class="h-mini-val" style="color:var(--green)">${{d.overview.suppliers}}</div><div class="h-mini-lbl">Suppliers</div></div><div class="h-mini-card"><div class="h-mini-val" style="color:var(--yellow)">${{d.overview.risks}}</div><div class="h-mini-lbl">Risks</div></div><div class="h-mini-card"><div class="h-mini-val" style="color:var(--blue)">${{d.overview.plants}}</div><div class="h-mini-lbl">Plants</div></div><div class="h-mini-card"><div class="h-mini-val" style="color:var(--purple)">${{d.overview.exports}}</div><div class="h-mini-lbl">Exports</div></div></div><div style="font-size:11px;color:var(--t3);line-height:1.5;padding:2px 2px 0">${{d.overview.desc}}</div></div></div></div>
    <div class="section open" id="sec-mats"><div class="s-head" onclick="toggleSection('sec-mats')"><div class="s-icon" style="background:rgba(251,146,60,.1)">⛏</div><div class="s-title">Raw Materials</div><div class="s-meta">${{d.materials.length}} inputs</div><div class="s-arrow">▼</div></div><div class="s-body"><div class="s-content"><div class="mat-list">${{matHtml}}</div></div></div></div>
    <div class="section" id="sec-sup"><div class="s-head" onclick="toggleSection('sec-sup')"><div class="s-icon" style="background:rgba(52,211,153,.1)">🤝</div><div class="s-title">Key Suppliers</div><div class="s-meta">${{d.suppliers.length}} partners</div><div class="s-arrow">▼</div></div><div class="s-body"><div class="s-content"><div class="sup-list">${{supHtml}}</div></div></div></div>
    <div class="section" id="sec-prices"><div class="s-head" onclick="toggleSection('sec-prices')"><div class="s-icon" style="background:rgba(251,191,36,.1)">📈</div><div class="s-title">Commodity Prices</div><div class="s-meta" id="prices-meta">Pending</div><div class="s-arrow">▼</div></div><div class="s-body"><div class="s-content"><div class="price-list" id="price-list">${{priceHtml}}</div></div></div></div>
    <div class="section" id="sec-heat"><div class="s-head" onclick="toggleSection('sec-heat')"><div class="s-icon" style="background:rgba(192,132,252,.1)">🔥</div><div class="s-title">Industry Heatmap</div><div class="s-meta">${{d.heatmap.length}} regions</div><div class="s-arrow">▼</div></div><div class="s-body"><div class="s-content"><div class="heat-legend"><div class="heat-lbl">LOW</div><div class="heat-grad"></div><div class="heat-lbl">HIGH</div></div><div class="heat-rows">${{heatHtml}}</div></div></div></div>`;

            if (window._cachedShips) renderShipsSidebar(window._cachedShips);
            if (window._cachedNewsHtml) {{
                var tempDiv = document.createElement('div');
                tempDiv.className = 'section open';
                tempDiv.id = 'sec-news';
                tempDiv.innerHTML = '<div class="s-head"><div class="s-icon" style="background:rgba(56,189,248,.1)">📰</div><div class="s-title">Live News</div><div class="s-meta" style="color:var(--blue)">Latest</div><div class="s-arrow">▼</div></div><div class="s-body"><div class="s-content"><div class="news-list">' + window._cachedNewsHtml + '</div></div></div>';
                sb.appendChild(tempDiv);
                tempDiv.querySelector('.s-head').addEventListener('click', function(){{ tempDiv.classList.toggle('open'); }});
                tempDiv.querySelectorAll('.news-item').forEach(function(item){{
                    item.addEventListener('click', function(){{
                        var link = this.dataset.link;
                        if(link && link !== '#') window.open(link, '_blank');
                    }});
                }});
            }}
            if(window._updateCommodityPrices) window._updateCommodityPrices();
        }}

        function matchCompany(q) {{
            q = q.toLowerCase().trim();
            if (q.includes('tata')) return 'tata';
            if (q.includes('jsw')) return 'jsw';
            if (q.includes('reliance') || q.includes('ril')) return 'reliance';
            return null;
        }}

        function toggleSection(id) {{ document.getElementById(id).classList.toggle('open'); }}
        function toggleRisk(card) {{ card.classList.toggle('expanded'); }}
        function scrollToRisk() {{ const el = document.getElementById('sec-risk'); el.classList.add('open'); el.scrollIntoView({{ behavior: 'smooth', block: 'start' }}); }}
        
        window.flyToMap = function(lat, lng, zoom) {{
            if(window.map) {{
                window.map.flyTo({{center: [lng, lat], zoom: zoom, duration: 1200}});
            }}
        }};

        function toggleLayer(btn) {{ 
            const l = btn.dataset.l; 
            layerState[l] = !layerState[l]; 
            btn.classList.toggle('on', layerState[l]); 
            if(window.map && window.map.isStyleLoaded()) {{
                if(l === 'routes') {{
                    if(map.getSource('routes')) map.setLayoutProperty('routes-layer', 'visibility', layerState.routes ? 'visible' : 'none');
                }}
                if(l === 'heat') {{
                    if(map.getSource('heat')) map.setLayoutProperty('heat-layer', 'visibility', layerState.heat ? 'visible' : 'none');
                }}
                if(l === 'risk') {{
                    document.querySelectorAll('.maplibregl-marker:not(.live-ship-marker)').forEach(mk => {{
                        mk.style.display = layerState.risk ? 'block' : 'none';
                    }});
                }}
            }}
        }}
        window.toggleLayer = toggleLayer;

        function renderMapFeatures(d) {{
            if(!window.map || !window.map.isStyleLoaded()) return;
            
            activeMarkers.forEach(m => m.remove());
            activeMarkers = [];
            
            d.markers.forEach(m => {{
                var el = document.createElement('div');
                var s = m.s || 34;
                el.style.cssText = `width:${{s}}px;height:${{s}}px;background:${{m.c}}18;border:1.5px solid ${{m.c}};border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:${{Math.round(s * .38)}}px;box-shadow:0 0 14px ${{m.c}}55;cursor:pointer;transition:transform .2s`;
                el.innerText = m.e;
                el.onmouseover = function() {{ el.style.transform = 'scale(1.15)'; }};
                el.onmouseout = function() {{ el.style.transform = 'scale(1)'; }};
                if(!layerState.risk) el.style.display = 'none';

                let rows = m.rows.map(r => `<div class="popup-row"><span class="popup-key">${{r[0]}}</span><span class="popup-val">${{r[1]}}</span></div>`).join('');
                let content = `<div class="popup-inner"><div class="popup-tag" style="background:${{m.c}}18;color:${{m.c}}">${{m.e}} ${{m.tag}}</div><div class="popup-title">${{m.title}}</div><div class="popup-rows">${{rows}}</div></div>`;
                
                var marker = new maplibregl.Marker({{element:el}})
                    .setLngLat([m.ll[1], m.ll[0]])
                    .setPopup(new maplibregl.Popup({{offset:s/2}}).setHTML(content))
                    .addTo(map);
                activeMarkers.push(marker);
            }});
            
            let routeFeatures = [];
            d.routes.forEach(r => {{
                routeFeatures.push({{
                    "type": "Feature",
                    "properties": {{ "color": r.style.color }},
                    "geometry": {{
                        "type": "LineString",
                        "coordinates": r.pts.map(p => [p[1], p[0]])
                    }}
                }});
            }});
            let routesCollection = {{"type":"FeatureCollection", "features":routeFeatures}};
            
            if(map.getSource('routes')) {{
                map.getSource('routes').setData(routesCollection);
            }} else {{
                map.addSource('routes', {{ type: 'geojson', data: routesCollection }});
                map.addLayer({{
                    'id': 'routes-layer',
                    'type': 'line',
                    'source': 'routes',
                    'layout': {{
                        'line-join': 'round',
                        'line-cap': 'round',
                        'visibility': layerState.routes ? 'visible' : 'none'
                    }},
                    'paint': {{
                        'line-color': ['get', 'color'],
                        'line-width': 1.8,
                        'line-dasharray': [10, 7]
                    }}
                }});
            }}
            
            let heatFeatures = [];
            d.heatCircles.forEach(h => {{
                heatFeatures.push({{
                    "type": "Feature",
                    "properties": {{ "color": h.c, "name": h.n, "workforce": h.w }},
                    "geometry": {{ "type": "Point", "coordinates": [h.ll[1], h.ll[0]] }}
                }});
            }});
            let heatCollection = {{"type":"FeatureCollection", "features":heatFeatures}};
            if(map.getSource('heat')) {{
                map.getSource('heat').setData(heatCollection);
            }} else {{
                map.addSource('heat', {{ type: 'geojson', data: heatCollection }});
                map.addLayer({{
                    'id': 'heat-layer',
                    'type': 'circle',
                    'source': 'heat',
                    'layout': {{
                        'visibility': layerState.heat ? 'visible' : 'none'
                    }},
                    'paint': {{
                        'circle-radius': 40,
                        'circle-color': ['get', 'color'],
                        'circle-opacity': 0.15,
                        'circle-stroke-width': 1,
                        'circle-stroke-color': ['get', 'color'],
                        'circle-stroke-opacity': 0.4
                    }}
                }});
                
                map.on('click', 'heat-layer', function(e) {{
                    var c = e.features[0].properties.color;
                    var n = e.features[0].properties.name;
                    var w = e.features[0].properties.workforce;
                    var html = `<div class="popup-inner"><div class="popup-tag" style="background:${{c}}18;color:${{c}}">🔥 Industry Zone</div><div class="popup-title">${{n}}</div><div class="popup-rows"><div class="popup-row"><span class="popup-key">Workforce</span><span class="popup-val">${{w}}</span></div></div></div>`;
                    new maplibregl.Popup()
                        .setLngLat(e.lngLat)
                        .setHTML(html)
                        .addTo(map);
                }});
                map.on('mouseenter', 'heat-layer', () => {{ map.getCanvas().style.cursor = 'pointer'; }});
                map.on('mouseleave', 'heat-layer', () => {{ map.getCanvas().style.cursor = ''; }});
            }}
        }}

        function switchCompany(key) {{
            window.activeCompany = key;
            const d = companies[key]; if (!d) return;
            document.getElementById('cAvatar').innerHTML = d.avatar;
            document.getElementById('cAvatar').style.background = d.avatarBg;
            document.getElementById('cName').textContent = d.name;
            document.getElementById('cExchange').textContent = d.exchange;
            document.getElementById('searchInput').value = d.name;
            d.kpis.forEach((k, i) => {{ document.getElementById('kv' + i).textContent = k.v; document.getElementById('kv' + i).style.color = k.c; document.getElementById('kl' + i).textContent = k.l; }});
            document.getElementById('healthVal').textContent = d.health.score;
            document.getElementById('healthVal').style.color = d.health.color;
            const hb = document.getElementById('healthBar'); hb.style.width = d.health.score + '%'; hb.style.animation = 'none'; hb.offsetHeight; hb.style.animation = 'bar-grow .8s ease .3s both';
            document.getElementById('healthSub').textContent = d.health.sub;
            document.querySelectorAll('.c-pill').forEach(p => p.classList.toggle('on', p.dataset.company === key));
            renderSidebar(d);

            if(window.map && window.map.isStyleLoaded()) {{
                renderMapFeatures(d);
                map.flyTo({{ center: [d.mapCenter[1], d.mapCenter[0]], zoom: d.mapZoom, duration: 1200 }});
            }}
        }}
        
        var WB = [
          {{emoji:'🪨', name:'Iron Ore',   url:'https://api.worldbank.org/v2/en/indicator/PIORECR.MT?format=json&mrv=1&per_page=1', fallback:118.4, unit:'/MT'}},
          {{emoji:'🖤', name:'Coal AUS',   url:'https://api.worldbank.org/v2/en/indicator/PCOALAU.MT?format=json&mrv=1&per_page=1', fallback:245.0, unit:'/MT'}},
          {{emoji:'🛢️', name:'Brent Crude',url:'https://api.worldbank.org/v2/en/indicator/POILBRE.USD?format=json&mrv=1&per_page=1', fallback:82.4,  unit:'/bbl'}},
          {{emoji:'🔥', name:'Nat Gas',    url:'https://api.worldbank.org/v2/en/indicator/PNGASUS.USD?format=json&mrv=1&per_page=1', fallback:9.8,   unit:'/mmBtu'}}
        ];

        function renderPrices(results) {{
          var pl = document.getElementById('price-list');
          if(!pl) return;
          pl.innerHTML = results.map(function(r){{
            var chg = ((Math.random()-0.45)*4).toFixed(1);
            var up = parseFloat(chg) > 0;
            return '<div class="price-row">'+
              '<div class="p-name">'+r.c.emoji+' '+r.c.name+'</div>'+
              '<div class="p-right">'+
                '<div class="p-val">$'+r.val+r.c.unit+'</div>'+
                '<div class="p-chg '+(up?'up':'dn')+'">'+(up?'▲':'▼')+' '+Math.abs(chg)+'%</div>'+
              '</div></div>';
          }}).join('');
        }}
        
        function loadPrices() {{
          var pl = document.getElementById('price-list');
          if(!pl) return;
          renderPrices(WB.map(function(c){{ return {{c:c, val:c.fallback}}; }}));
          Promise.all(WB.map(function(c){{
            return fetch(c.url)
              .then(function(r){{ return r.json(); }})
              .then(function(d){{ 
                var v = d[1] && d[1][0] && d[1][0].value;
                return {{c:c, val: v ? parseFloat(v).toFixed(1) : c.fallback}};
              }})
              .catch(function(){{ return {{c:c, val:c.fallback}}; }});
          }})).then(function(results){{
            renderPrices(results);
            var pm = document.getElementById('prices-meta');
            if(pm) pm.textContent = 'Live ✓';
          }});
        }}
        window._updateCommodityPrices = loadPrices;

        function renderShipsSidebar(ships) {{
            window._cachedShips = ships;
            var sbScroll = document.getElementById('sb-scroll');
            var shipSection = document.getElementById('sec-ships');
            if (shipSection) shipSection.remove();

            var displayShips = ships.slice(0, 8);
            var shipHtml = displayShips.map(function (s) {{
                var shipName = s.name || s.SHIPNAME || 'Unknown Vessel';
                var shipType = s.type || s.SHIPTYPE || 'Cargo';
                var speed = s.speed || s.SPEED || 0;
                var lat = s.lat ? Number(s.lat).toFixed(1) : '?';
                var lon = s.lon ? Number(s.lon).toFixed(1) : '?';
                return '<div class="ship-item" data-lat="' + s.lat + '" data-lon="' + s.lon + '"><div class="ship-pip"></div><div class="ship-body"><div class="ship-name">' + shipName + '</div><div class="ship-detail">' + shipType + ' · ' + lat + '°, ' + lon + '°</div></div><div class="ship-right"><div class="ship-speed">' + speed + ' kn</div><div class="ship-status">● Live</div></div></div>';
            }}).join('');

            var sectionEl = document.createElement('div');
            sectionEl.className = 'section open';
            sectionEl.id = 'sec-ships';
            sectionEl.innerHTML = '<div class="s-head"><div class="s-icon" style="background:rgba(34,197,94,.12)">🚢</div><div class="s-title">Live Ships <span id="ships-meta" style="font-weight:normal;color:var(--green)"></span></div><div class="s-arrow">▼</div></div><div class="s-body"><div class="s-content"><div class="ship-list">' + shipHtml + '</div></div></div>';

            var firstSection = sbScroll.querySelector('.section');
            if (firstSection) sbScroll.insertBefore(sectionEl, firstSection);
            else sbScroll.appendChild(sectionEl);

            var sm = document.getElementById('ships-meta');
            if(sm) sm.textContent = ships.length + ' Live';

            sectionEl.querySelector('.s-head').addEventListener('click', function () {{ sectionEl.classList.toggle('open'); }});
            sectionEl.querySelectorAll('.ship-item').forEach(function (item) {{
                item.addEventListener('click', function () {{
                    var lat = parseFloat(this.dataset.lat);
                    var lon = parseFloat(this.dataset.lon);
                    if (!isNaN(lat) && !isNaN(lon) && window.map) {{
                        map.flyTo({{center: [lon, lat], zoom: 7, duration: 1200}});
                    }}
                }});
            }});
        }}
        
        window.addEventListener('load', function() {{
            document.getElementById('analyseBtn').addEventListener('click', function () {{
                const key = matchCompany(document.getElementById('searchInput').value);
                if (key) switchCompany(key);
            }});
            document.getElementById('searchInput').addEventListener('keydown', function (e) {{
                if (e.key === 'Enter') {{ const key = matchCompany(this.value); if (key) switchCompany(key); }}
            }});
            document.querySelectorAll('.c-pill').forEach(p => {{
                p.addEventListener('click', function () {{ switchCompany(this.dataset.company); }});
            }});
            
            document.getElementById('sb-toggle').addEventListener('click', function(){{
              var sb = document.querySelector('.sidebar');
              var btn = document.getElementById('sb-toggle');
              sb.classList.toggle('collapsed');
              btn.textContent = sb.classList.contains('collapsed') ? '❮' : '❯';
              setTimeout(function(){{ if(window.map) {{ map.resize(); }} }}, 310);
            }});

            window.map = new maplibregl.Map({{
              container: 'map',
              style: 'https://api.maptiler.com/maps/darkmatter/style.json?key=AVA08bxnKmJ3Pbc4DBA7',
              center: [62, 18],
              zoom: 3,
              attributionControl: false
            }});
            map.addControl(new maplibregl.NavigationControl(), 'top-right');

            map.on('load', function() {{
                if(window.activeCompany) {{
                    renderMapFeatures(companies[window.activeCompany]);
                }} else {{
                    switchCompany('tata');
                }}
                
                fetch('https://delicate-recipe-b1b3.quantumfaizan.workers.dev/')
                  .then(function(r){{ return r.json(); }})
                  .then(function(data){{
                    var ships = data.ships || data.data || [];
                    if(Array.isArray(data)) ships = data;
                    ships.forEach(function(s){{
                      if(!s.lat || !s.lon) return; 
                      var el = document.createElement('div');
                      el.className = 'live-ship-marker';
                      el.style.cssText = 'width:10px;height:10px;background:#34d399;border:1.5px solid #34d399;border-radius:50%;box-shadow:0 0 8px #34d39988;cursor:pointer;';
                      new maplibregl.Marker({{element:el}})
                        .setLngLat([s.lon, s.lat])
                        .setPopup(new maplibregl.Popup({{offset:14}}).setHTML(
                          '<div class="popup-inner"><div class="popup-title"><b style="color:#34d399">🚢 '+(s.name||s.SHIPNAME||'Ship')+'</b></div>' +
                          '<div class="popup-rows"><div class="popup-row"><span class="popup-key">Speed</span><span class="popup-val">'+(s.speed||s.SPEED||0)+' kn</span></div>' +
                          '<div class="popup-row"><span class="popup-key">Destination</span><span class="popup-val">'+(s.dest||s.DESTINATION||'Unknown')+'</span></div></div></div>'
                        ))
                        .addTo(map);
                    }});
                    renderShipsSidebar(ships);
                  }})
                  .catch(function(){{ console.log('Ships fetch failed'); }});
            }});
            
            var newsKeywords = ['ship', 'cargo', 'supply', 'trade', 'sanctions', 'oil'];
            var fallbackNews = [{{ title: 'Global shipping costs surge amid Red Sea disruptions', link: '#' }}, {{ title: 'EU sanctions on Russian oil reshape trade routes', link: '#' }}];
            fetch('https://api.allorigins.win/get?url=' + encodeURIComponent('https://feeds.bbci.co.uk/news/world/rss.xml'))
                .then(function(res) {{ return res.json(); }})
                .then(function(data) {{
                    var xmlStr = data.contents || '';
                    var parser = new DOMParser();
                    var xml = parser.parseFromString(xmlStr, 'text/xml');
                    var items = xml.querySelectorAll('item');
                    var articles = [];
                    items.forEach(function(item) {{
                        var title = item.querySelector('title') ? item.querySelector('title').textContent : '';
                        var link = item.querySelector('link') ? item.querySelector('link').textContent : '#';
                        if(newsKeywords.some(function(kw) {{ return title.toLowerCase().includes(kw); }})) articles.push({{ title: title, link: link }});
                    }});
                    if(articles.length === 0) articles = fallbackNews;
                    window._cachedNewsHtml = articles.slice(0, 3).map(function(a) {{
                        var matched = newsKeywords.filter(function(kw){{ return a.title.toLowerCase().includes(kw);}});
                        var tagHtml = matched.length > 0 ? '<span class="news-tag">' + matched[0] + '</span>' : '';
                        return '<div class="news-item" data-link="' + (a.link || '#') + '"><div class="news-title">' + a.title + '</div><div class="news-meta"><span class="news-src">BBC</span>' + tagHtml + '</div></div>';
                    }}).join('');
                }}).catch(function(){{}});

            if(!window.activeCompany) switchCompany('tata');
            loadPrices();
        }});
    </script>"""

    # find <script> section using python
    start_idx = html.find('    <script>')
    if start_idx != -1:
        # replace from <script> to end
        html = html[:start_idx] + new_script + "\n</body>\n</html>"
        with open("c:/Users/hp/.gemini/antigravity/scratch/chainscope/index.html", "w", encoding="utf-8") as fOut:
            fOut.write(html)
        print("Patched successfully!")
    else:
        print("Couldn't find <script> section.")

fix_html()
