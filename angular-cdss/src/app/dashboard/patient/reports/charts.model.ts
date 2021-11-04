export default interface ChartSettings {
    chartType: "bar" | "line" | "pie" | "stack"; 
    scheme: {
        domain: string[]
    };
    legend: boolean;
    animations: boolean;
    
    // bar/line only
    xAxis?: boolean;
    yAxis?: boolean;
    showYAxisLabel?: boolean;
    showXAxisLabel?: boolean;
    xAxisLabel?: string;
    yAxisLabel?: string;
    
    // bar only
    showDataLabel?: boolean;
    roundEdges?: boolean;
    
    // line only
    timeline?: boolean;

    // pie only
    showLabels?: boolean;
}