import React, { useState } from "react"
import Home from "./pages/Home"
import Dashboard from "./pages/Dashboard"

export default function App() {
  const [page, setPage] = useState("home")
  const [resultData, setResultData] = useState(null)

  const goDashboard = () => setPage("dashboard")
  const goHome = () => setPage("home")

  return (
    <>
      {page === "home" && <Home goDashboard={goDashboard} />}
      {page === "dashboard" && (
        <Dashboard 
          goHome={goHome}
          resultData={resultData}
          setResultData={setResultData}
        />
      )}
    </>
  )
}
