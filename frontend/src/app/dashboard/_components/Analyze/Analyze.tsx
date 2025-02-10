"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

export default function AnalyzeComponent() {
	const [progress, setProgress] = useState(0)
	const [isAnalyzing, setIsAnalyzing] = useState(true)

	useEffect(() => {
		if (isAnalyzing) {
			const timer = setInterval(() => {
				setProgress((oldProgress) => {
					const newProgress = oldProgress + 2
					if (newProgress === 100) {
						clearInterval(timer)
						setIsAnalyzing(false)
					}
					return Math.min(newProgress, 100)
				})
			}, 100)

			return () => clearInterval(timer)
		}
	}, [isAnalyzing])

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
							<Button className="w-full" size="lg" onClick={() => console.log("Show insights clicked")}>
								Show Insights
							</Button>
						</div>
					)}
				</div>
			</Card>
		</div>
	)
}

