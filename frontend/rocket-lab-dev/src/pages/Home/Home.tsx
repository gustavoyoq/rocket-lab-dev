import type { ReactNode } from 'react'
import { useEffect, useState } from 'react'
import { Button } from '../../components/ui/Button'
import { DeleteProductDialog } from '../../components/products/DeleteProductDialog'
import { Pagination } from '../../components/products/Pagination'
import { ProductCard } from '../../components/products/ProductCard'
import { ProductFormModal } from '../../components/products/ProductFormModal'
import { ProductToolbar } from '../../components/products/ProductToolbar'
import { useProducts, toFormValues } from '../../hooks/useProducts'
import type { ProductListingItem, ProductFormValues } from '../../types/product'

const PAGE_SIZE = 24

export function Home() {
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState('all')
  const [currentPage, setCurrentPage] = useState(1)
  const {
    products,
    categories,
    totalPages,
    totalItems,
    loading,
    error,
    reload,
    createProduct,
    updateProduct,
    deleteProduct,
  } = useProducts({
    page: currentPage,
    pageSize: PAGE_SIZE,
    search,
    category,
  })
  const [isCreateOpen, setIsCreateOpen] = useState(false)
  const [editingProduct, setEditingProduct] = useState<ProductListingItem | null>(null)
  const [deletingProduct, setDeletingProduct] = useState<ProductListingItem | null>(null)

  useEffect(() => {
    if (currentPage > totalPages) {
      setCurrentPage(totalPages)
    }
  }, [currentPage, totalPages])

  function handleSearchChange(value: string) {
    setSearch(value)
    setCurrentPage(1)
  }

  function handleCategoryChange(value: string) {
    setCategory(value)
    setCurrentPage(1)
  }

  async function handleCreate(values: ProductFormValues) {
    await createProduct(values)
    setIsCreateOpen(false)
  }

  async function handleUpdate(values: ProductFormValues) {
    if (!editingProduct) {
      return
    }

    await updateProduct(editingProduct.id_produto, values)
    setEditingProduct(null)
  }

  async function handleDelete() {
    if (!deletingProduct) {
      return
    }

    await deleteProduct(deletingProduct.id_produto)
    setDeletingProduct(null)
  }

  return (
    <section className="space-y-6">
      <div className="space-y-2 pt-2">
        <p className="text-sm font-semibold uppercase tracking-[0.22em] text-[#6b8f4a]">Catálogo PackIt</p>
        <h2 className="text-3xl font-semibold text-slate-900">Produtos em destaque</h2>
        <p className="max-w-3xl text-sm text-slate-600">
          Navegue, filtre, edite e acompanhe métricas dos produtos do catálogo.
        </p>
      </div>

      <ProductToolbar
        search={search}
        category={category}
        categories={categories}
        onSearchChange={handleSearchChange}
        onCategoryChange={handleCategoryChange}
        onAddProduct={() => setIsCreateOpen(true)}
      />

      {loading ? (
        <StateBox>Carregando produtos...</StateBox>
      ) : error ? (
        <StateBox variant="error">
          <p>{error}</p>
          <Button variant="secondary" onClick={reload}>
            Tentar novamente
          </Button>
        </StateBox>
      ) : products.length === 0 ? (
        <StateBox>Nenhum produto encontrado.</StateBox>
      ) : (
        <>
          <p className="text-sm text-slate-500">
            Exibindo página {currentPage} de {totalPages} ({totalItems} produtos encontrados)
          </p>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-6">
            {products.map((product) => (
              <ProductCard
                key={product.id_produto}
                product={product}
                onEdit={() => setEditingProduct(product)}
                onDelete={() => setDeletingProduct(product)}
              />
            ))}
          </div>

          <Pagination
            currentPage={currentPage}
            totalPages={totalPages}
            onPrevious={() => setCurrentPage((page) => Math.max(1, page - 1))}
            onNext={() => setCurrentPage((page) => Math.min(totalPages, page + 1))}
            onGoToPage={(page) => setCurrentPage(page)}
          />
        </>
      )}

      {isCreateOpen ? (
        <ProductFormModal
          title="Adicionar produto"
          categories={categories}
          initialValues={blankProductForm}
          onClose={() => setIsCreateOpen(false)}
          onSubmit={handleCreate}
          submitLabel="Adicionar"
        />
      ) : null}

      {editingProduct ? (
        <ProductFormModal
          title="Editar produto"
          categories={categories}
          initialValues={toFormValues(editingProduct)}
          onClose={() => setEditingProduct(null)}
          onSubmit={handleUpdate}
          submitLabel="Editar"
        />
      ) : null}

      {deletingProduct ? (
        <DeleteProductDialog
          productName={deletingProduct.nome_produto}
          onClose={() => setDeletingProduct(null)}
          onDelete={handleDelete}
        />
      ) : null}
    </section>
  )
}

function StateBox({ children, variant = 'default' }: { children: ReactNode; variant?: 'default' | 'error' }) {
  return (
    <div
      className={`flex min-h-56 flex-col items-center justify-center gap-4 rounded-3xl border px-6 py-10 text-center ${
        variant === 'error' ? 'border-rose-200 bg-rose-50 text-rose-700' : 'border-[#99d98c] bg-[#b5e48c] text-slate-800'
      }`}
    >
      {children}
    </div>
  )
}

const blankProductForm: ProductFormValues = {
  nome_produto: '',
  categoria_produto: '',
  imagem_url: '',
  peso_produto_gramas: '',
  comprimento_centimetros: '',
  altura_centimetros: '',
  largura_centimetros: '',
}
