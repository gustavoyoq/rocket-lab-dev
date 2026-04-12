import { Button } from '../ui/Button'
import { Modal } from '../ui/Modal'

interface DeleteProductDialogProps {
  productName: string
  onClose: () => void
  onDelete: () => Promise<void> | void
}

export function DeleteProductDialog({ productName, onClose, onDelete }: DeleteProductDialogProps) {
  return (
    <Modal
      title="Deletar produto"
      onClose={onClose}
      actions={
        <>
          <Button variant="secondary" onClick={onClose} type="button">
            Cancelar
          </Button>
          <Button variant="danger" onClick={onDelete} type="button">
            Deletar
          </Button>
        </>
      }
    >
      <p className="text-sm text-slate-700">Você quer mesmo deletar o produto <strong>{productName}</strong>?</p>
    </Modal>
  )
}
