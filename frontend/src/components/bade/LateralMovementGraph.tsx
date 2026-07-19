import { useEffect, useRef } from 'react';
import * as d3 from 'd3';

export default function LateralMovementGraph() {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current) return;
    
    const width = svgRef.current.clientWidth;
    const height = 200;

    const nodes = [
      { id: 'WORKSTATION-HR-01', group: 'compromised', x: width * 0.1, y: height / 2 },
      { id: 'FILE-SERVER-02', group: 'suspicious', x: width * 0.4, y: height / 2 },
      { id: 'DOMAIN-CONTROLLER-01', group: 'targeted', x: width * 0.7, y: height / 2 },
      { id: 'AIIMS-EMR-SERVER', group: 'safe', x: width * 0.9, y: height / 2 }
    ];

    const links = [
      { source: nodes[0], target: nodes[1] },
      { source: nodes[1], target: nodes[2] },
      { source: nodes[2], target: nodes[3] }
    ];

    const svg = d3.select(svgRef.current);
    svg.selectAll("*").remove();

    // Draw links
    svg.append("g")
      .selectAll("line")
      .data(links)
      .enter().append("line")
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y)
      .attr("stroke", "#ff3366")
      .attr("stroke-width", 2)
      .attr("stroke-dasharray", "5,5")
      .attr("class", "animate-pulse");

    // Draw nodes
    const node = svg.append("g")
      .selectAll("circle")
      .data(nodes)
      .enter().append("circle")
      .attr("r", 15)
      .attr("cx", d => d.x)
      .attr("cy", d => d.y)
      .attr("fill", d => d.group === 'compromised' ? '#ff3366' : d.group === 'suspicious' ? '#ff9900' : d.group === 'targeted' ? '#eab308' : '#00ff88')
      .attr("class", d => d.group === 'compromised' ? 'glow-red animate-pulse' : '');

    // Draw labels
    svg.append("g")
      .selectAll("text")
      .data(nodes)
      .enter().append("text")
      .attr("x", d => d.x)
      .attr("y", d => d.y + 30)
      .attr("text-anchor", "middle")
      .attr("fill", "#8899aa")
      .attr("font-size", "10px")
      .attr("font-family", "monospace")
      .text(d => d.id);

  }, []);

  return (
    <div className="glass rounded-xl p-4 h-[250px] flex flex-col">
      <h3 className="font-bold text-lg mb-2">Lateral Movement Chain</h3>
      <div className="flex-1 w-full relative">
        <svg ref={svgRef} className="w-full h-full" />
      </div>
    </div>
  );
}
