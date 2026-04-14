import { useEffect, useState } from 'react'
import { FaAngleLeft, FaAngleRight } from 'react-icons/fa'
import { Button } from '../ui/Button'

interface PaginationProps {
  currentPage: number
  totalPages: number
  onPrevious: () => void
  onNext: () => void
  onGoToPage: (page: number) => void
}

export function Pagination({ currentPage, totalPages, onPrevious, onNext, onGoToPage }: PaginationProps) {
  const [pageInput, setPageInput] = useState(String(currentPage))

  useEffect(() => {
    setPageInput(String(currentPage))
  }, [currentPage])

  function commitPageInput() {
    const pageNumber = Number(pageInput)
    if (!Number.isFinite(pageNumber)) {
      setPageInput(String(currentPage))
      return
    }

    const nextPage = Math.min(Math.max(1, Math.trunc(pageNumber)), totalPages)
    setPageInput(String(nextPage))
    onGoToPage(nextPage)
  }

  return (
    <div className="mt-6">
      <div className="flex items-center justify-center gap-3">
        <Button
          variant="secondary"
          onClick={onPrevious}
          disabled={currentPage <= 1}
          aria-label="Pagina anterior"
          className="cursor-pointer disabled:cursor-not-allowed"
        >
          <FaAngleLeft aria-hidden="true" />
        </Button>

        <div className="inline-flex items-center gap-2 rounded-full bg-[#a4ef8e] px-3 py-2 text-sm font-semibold text-slate-800 ring-1 ring-[#99d98c]">
          <input
            type="number"
            min={1}
            max={totalPages}
            value={pageInput}
            onChange={(event) => setPageInput(event.target.value)}
            onBlur={commitPageInput}
            onKeyDown={(event) => {
              if (event.key === 'Enter') {
                event.preventDefault()
                commitPageInput()
              }
            }}
            aria-label="Página atual"
            className="w-14 bg-transparent text-center text-sm font-semibold text-slate-800 outline-none"
          />
          <span className="text-slate-700">/ {totalPages}</span>
        </div>

        <Button
          variant="secondary"
          onClick={onNext}
          disabled={currentPage >= totalPages}
          aria-label="Proxima pagina"
          className="cursor-pointer disabled:cursor-not-allowed"
        >
          <FaAngleRight aria-hidden="true" />
        </Button>
      </div>
    </div>
  )
}
