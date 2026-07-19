import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { AttackPath, NetworkNode, NetworkEdge } from '../../types';

export default function AttackPathGraph({ topology, isSimulating }: { topology: AttackPath, isSimulating: boolean }) {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!svgRef.current || !containerRef.current || !topology.nodes.length) return;

    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    // Zoom setup
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.5, 4])
      .on("zoom", (event) => {
        g.attr("transform", event.transform);
      });
    svg.call(zoom);

    const g = svg.append("g");

    // Simulation
    const simulation = d3.forceSimulation(topology.nodes as any)
      .force("link", d3.forceLink(topology.edges).id((d: any) => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collide", d3.forceCollide().radius(30));

    // Links
    const link = g.append("g")
      .selectAll("line")
      .data(topology.edges)
      .enter().append("line")
      .attr("stroke", d => d.status === 'unprotected' ? '#ff3366' : d.status === 'weak' ? '#ff9900' : '#1e2d42')
      .attr("stroke-width", d => d.status === 'unprotected' ? 3 : 2)
      .attr("stroke-opacity", 0.6)
      .attr("class", d => d.status === 'unprotected' && isSimulating ? 'animate-pulse' : '');

    // Nodes
    const node = g.append("g")
      .selectAll("g")
      .data(topology.nodes)
      .enter().append("g")
      .call(d3.drag<SVGGElement, any>()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

    // Shapes based on type
    node.each(function(d: NetworkNode) {
      const el = d3.select(this);
      const size = 15 + d.criticality * 2;
      const color = d.status === 'compromised' ? '#ff3366' : d.status === 'weak' ? '#ff9900' : '#00d4ff';

      if (d.isChokepoint) {
        el.append("circle")
          .attr("r", size + 8)
          .attr("fill", "none")
          .attr("stroke", "#00d4ff")
          .attr("stroke-width", 2)
          .attr("stroke-dasharray", "4 4")
          .attr("class", "animate-spin-slow");
      }

      if (d.type === 'server') {
        el.append("rect").attr("width", size*2).attr("height", size*2).attr("x", -size).attr("y", -size).attr("fill", color);
      } else if (d.type === 'workstation') {
        el.append("circle").attr("r", size).attr("fill", color);
      } else if (d.type === 'ot') {
        el.append("polygon").attr("points", `0,-${size} ${size},0 0,${size} -${size},0`).attr("fill", color);
      } else {
        el.append("polygon").attr("points", `-${size},-${size} ${size},-${size} ${size/2},${size} -${size/2},${size}`).attr("fill", color);
      }
      
      if (d.status === 'compromised') {
        el.select("*").attr("class", "glow-red animate-pulse");
      }
    });

    // Labels
    node.append("text")
      .attr("dy", d => 25 + d.criticality * 2)
      .attr("text-anchor", "middle")
      .attr("fill", "#f0f4ff")
      .attr("font-size", "10px")
      .attr("font-family", "monospace")
      .text(d => d.label);

    simulation.on("tick", () => {
      link
        .attr("x1", (d: any) => d.source.x)
        .attr("y1", (d: any) => d.source.y)
        .attr("x2", (d: any) => d.target.x)
        .attr("y2", (d: any) => d.target.y);

      node.attr("transform", (d: any) => `translate(${d.x},${d.y})`);
    });

    function dragstarted(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event: any, d: any) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

  }, [topology, isSimulating]);

  return (
    <div className="glass rounded-xl h-full w-full relative overflow-hidden" ref={containerRef}>
      <div className="absolute top-4 left-4 z-10 bg-bg-secondary/80 p-2 rounded border border-border-subtle text-xs flex flex-col gap-2">
        <div className="font-bold mb-1">Legend</div>
        <div className="flex items-center gap-2"><div className="w-3 h-3 bg-accent-cyan rounded-full" /> Workstation</div>
        <div className="flex items-center gap-2"><div className="w-3 h-3 bg-accent-cyan" /> Server</div>
        <div className="flex items-center gap-2"><div className="w-3 h-3 bg-accent-cyan rotate-45" /> OT Device</div>
        <div className="flex items-center gap-2"><div className="w-3 h-3 border border-danger bg-danger/50 rounded-full" /> Compromised</div>
        <div className="flex items-center gap-2"><div className="w-4 h-4 border-2 border-accent-cyan border-dashed rounded-full" /> Chokepoint</div>
      </div>
      
      <svg ref={svgRef} className="w-full h-full bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-90" />
      
      {/* HUD overlay */}
      <div className="absolute inset-0 pointer-events-none border-2 border-accent-cyan/10 rounded-xl"></div>
    </div>
  );
}
