import { useEffect, useState, type FormEvent } from 'react'
import type { ProductFormValues } from '../../types/product'
import { Button } from '../ui/Button'
import { Input } from '../ui/Input'
import { Modal } from '../ui/Modal'
import { Select } from '../ui/Select'
import { getCategoryLabel } from '../../lib/category'

interface ProductFormModalProps {
  title: string
  categories: string[]
  initialValues: ProductFormValues
  onClose: () => void
  onSubmit: (values: ProductFormValues) => Promise<void> | void
  submitLabel: string
  onCancelLabel?: string
}

export function ProductFormModal({
  title,
  categories,
  initialValues,
  onClose,
  onSubmit,
  submitLabel,
  onCancelLabel = 'Cancelar',
}: ProductFormModalProps) {
  const [values, setValues] = useState(initialValues)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    setValues(initialValues)
  }, [initialValues])

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setSubmitting(true)

    try {
      await onSubmit(values)
      onClose()
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Modal
      title={title}
      onClose={onClose}
      actions={
        <>
          <Button variant="secondary" onClick={onClose} type="button">
            {onCancelLabel}
          </Button>
          <Button type="submit" form="product-form" disabled={submitting}>
            {submitting ? 'Salvando...' : submitLabel}
          </Button>
        </>
      }
    >
      <form id="product-form" className="grid gap-4 md:grid-cols-2" onSubmit={handleSubmit}>
        <label className="grid gap-2 md:col-span-2">
          <span className="text-sm font-medium text-slate-700">Nome do produto</span>
          <Input value={values.nome_produto} onChange={(event) => setValues({ ...values, nome_produto: event.target.value })} required />
        </label>
        <label className="grid gap-2 md:col-span-2">
          <span className="text-sm font-medium text-slate-700">Categoria</span>
          <Select value={values.categoria_produto} onChange={(event) => setValues({ ...values, categoria_produto: event.target.value })} required>
            <option value="">Selecione uma categoria</option>
            {categories.map((category) => (
              <option key={category} value={category}>
                {getCategoryLabel(category)}
              </option>
            ))}
          </Select>
        </label>
        <label className="grid gap-2 md:col-span-2">
          <span className="text-sm font-medium text-slate-700">Imagem do produto (URL)</span>
          <Input value={values.imagem_url} onChange={(event) => setValues({ ...values, imagem_url: event.target.value })} placeholder="https://..." />
        </label>
        {(['peso_produto_gramas', 'altura_centimetros', 'comprimento_centimetros', 'largura_centimetros'] as const).map((field) => (
          <label key={field} className="grid gap-2">
            <span className="text-sm font-medium text-slate-700">{labelMap[field]}</span>
            <Input
              type="number"
              min="0"
              step="0.01"
              value={values[field]}
              onChange={(event) => setValues({ ...values, [field]: event.target.value })}
            />
          </label>
        ))}
      </form>
    </Modal>
  )
}

const labelMap: Record<'peso_produto_gramas' | 'altura_centimetros' | 'comprimento_centimetros' | 'largura_centimetros', string> = {
  peso_produto_gramas: 'Peso do produto',
  altura_centimetros: 'Altura do produto',
  comprimento_centimetros: 'Comprimento do produto',
  largura_centimetros: 'Largura do produto',
}
