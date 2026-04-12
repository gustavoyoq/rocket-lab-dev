import type { PropsWithChildren, ReactNode } from 'react'

interface ModalProps extends PropsWithChildren {
  title: string
  onClose: () => void
  actions?: ReactNode
}

export function Modal({ title, onClose, actions, children }: ModalProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/50 px-4 py-6 backdrop-blur-sm">
      <div className="w-full max-w-3xl overflow-hidden rounded-3xl bg-[#b5e48c] shadow-2xl ring-1 ring-[#99d98c]">
        <div className="flex items-center justify-between border-b border-[#99d98c] px-6 py-4">
          <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
          <button className="text-2xl leading-none text-slate-500 transition hover:text-slate-900" onClick={onClose} type="button">
            ×
          </button>
        </div>
        <div className="px-6 py-5">{children}</div>
        {actions ? <div className="flex items-center justify-end gap-3 border-t border-[#99d98c] px-6 py-4">{actions}</div> : null}
      </div>
    </div>
  )
}
