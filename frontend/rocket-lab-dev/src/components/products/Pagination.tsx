import { useEffect, useRef, useState } from 'react'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'

interface PaginationProps {
  currentPage: number
  totalPages: number
  onPrevious: () => void
  onNext: () => void
  onGoToPage: (page: number) => void
}

export function Pagination({ currentPage, totalPages, onPrevious, onNext, onGoToPage }: PaginationProps) {
  const [pageInput, setPageInput] = useState(String(currentPage))
  const [isPagePickerOpen, setIsPagePickerOpen] = useState(false)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    setPageInput(String(currentPage))
  }, [currentPage])

  useEffect(() => {
    if (isPagePickerOpen) {
      inputRef.current?.focus()
      inputRef.current?.select()
    }
  }, [isPagePickerOpen])

  function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const pageNumber = Number(pageInput)
    if (!Number.isFinite(pageNumber)) {
      return
    }

    const nextPage = Math.min(Math.max(1, Math.trunc(pageNumber)), totalPages)
    onGoToPage(nextPage)
    setIsPagePickerOpen(false)
  }

  return (
    <div className="mt-6 space-y-4">
      <div className="flex items-center justify-center gap-3">
        <Button variant="secondary" onClick={onPrevious} disabled={currentPage <= 1} aria-label="Pagina anterior">
          ←
        </Button>
        <button
          type="button"
          onClick={() => setIsPagePickerOpen((current) => !current)}
          aria-label="Abrir seletor de página"
          className="min-w-12 rounded-full bg-white px-4 py-2 text-sm font-semibold text-slate-700 shadow-sm ring-1 ring-slate-200 transition hover:bg-slate-50"
        >
          {currentPage} / {totalPages}
        </button>
        <Button variant="secondary" onClick={onNext} disabled={currentPage >= totalPages} aria-label="Proxima pagina">
          →
        </Button>
      </div>

      {isPagePickerOpen ? (
        <form
          onSubmit={handleSubmit}
          className="mx-auto flex max-w-md flex-col gap-3 rounded-3xl bg-white px-4 py-4 shadow-sm ring-1 ring-slate-200 sm:flex-row sm:items-center"
        >
          <label className="flex-1 text-sm font-medium text-slate-700">
            Ir para página
            <Input
              ref={inputRef}
              type="number"
              min={1}
              max={totalPages}
              value={pageInput}
              onChange={(event) => setPageInput(event.target.value)}
              className="mt-2"
              aria-label="Ir para página específica"
            />
          </label>
          <Button type="submit" variant="secondary" className="sm:self-end">
            Ir
          </Button>
        </form>
      ) : null}
    </div>
  )
}
