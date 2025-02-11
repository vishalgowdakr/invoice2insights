"use client"

import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

interface AnalyzeComponentProps {
	progress: number;
	isAnalyzing: boolean;
	setActiveView: React.Dispatch<React.SetStateAction<string>>
}

export default function AnalyzeComponent({ progress, isAnalyzing, setActiveView }: AnalyzeComponentProps) {

	return (
		<div className="w-full max-w-md p-4 m-auto">
			<Card className="p-6 bg-white/95 backdrop-blur-sm shadow-lg">
				<div className="space-y-6">
					{isAnalyzing ? (
						<div className="space-y-4">
							<h3 className="text-lg font-medium text-center">Analyzing your document...</h3>
							<Progress value={progress} className="w-full h-2" />
							<p className="text-sm text-muted-foreground text-center">{progress}% complete</p>
						</div>
					) : (
						<div className="space-y-4">
							<h3 className="text-lg font-medium text-center text-green-600">Analysis Complete!</h3>
							<Button className="w-full" size="lg" onClick={() => setActiveView('dashboard')}>
								Show Insights
							</Button>
						</div>
					)}
				</div>
			</Card>
		</div>
	)
}
