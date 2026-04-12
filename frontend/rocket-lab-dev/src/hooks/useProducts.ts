import { useEffect, useState } from 'react'
import { createProduct, deleteProduct, listProductCategories, listProducts, updateProduct } from '../services/products'
import type { ProductFormValues, ProductInput, ProductListingItem } from '../types/product'

function extractErrorMessage(error: unknown, fallback: string) {
  if (typeof error === 'object' && error !== null && 'response' in error) {
    const responseData = (error as { response?: { data?: { detail?: string } } }).response?.data
    if (responseData?.detail) {
      return responseData.detail
    }
  }

  return fallback
}

function isNumeric(value: string): number | null {
  if (value.trim() === '') {
    return null
  }

  const parsed = Number(value)
  return Number.isNaN(parsed) ? null : parsed
}

export function formValuesToPayload(id: string, values: ProductFormValues): ProductInput {
  return {
    id_produto: id,
    nome_produto: values.nome_produto.trim(),
    categoria_produto: values.categoria_produto.trim(),
    imagem_url: values.imagem_url.trim() === '' ? null : values.imagem_url.trim(),
    peso_produto_gramas: isNumeric(values.peso_produto_gramas),
    comprimento_centimetros: isNumeric(values.comprimento_centimetros),
    altura_centimetros: isNumeric(values.altura_centimetros),
    largura_centimetros: isNumeric(values.largura_centimetros),
  }
}

export function toFormValues(product?: ProductListingItem | null): ProductFormValues {
  return {
    nome_produto: product?.nome_produto ?? '',
    categoria_produto: product?.categoria_produto ?? '',
    imagem_url: product?.imagem_url ?? '',
    peso_produto_gramas: product?.peso_produto_gramas?.toString() ?? '',
    comprimento_centimetros: product?.comprimento_centimetros?.toString() ?? '',
    altura_centimetros: product?.altura_centimetros?.toString() ?? '',
    largura_centimetros: product?.largura_centimetros?.toString() ?? '',
  }
}

interface UseProductsParams {
  page: number
  pageSize: number
  search: string
  category: string
}

export function useProducts({ page, pageSize, search, category }: UseProductsParams) {
  const [products, setProducts] = useState<ProductListingItem[]>([])
  const [categories, setCategories] = useState<string[]>([])
  const [totalPages, setTotalPages] = useState(1)
  const [totalItems, setTotalItems] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  async function loadProducts() {
    setLoading(true)
    setError(null)

    try {
      const [productsPage, categoryList] = await Promise.all([
        listProducts({ page, pageSize, search, category }),
        listProductCategories(),
      ])

      setProducts(productsPage.items)
      setTotalPages(productsPage.totalPages)
      setTotalItems(productsPage.totalItems)
      setCategories(categoryList)
    } catch {
      setError('Nao foi possivel carregar os produtos no momento.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadProducts()
  }, [page, pageSize, search, category])

  async function handleCreate(values: ProductFormValues) {
    const payload = formValuesToPayload(crypto.randomUUID().replace(/-/g, '').slice(0, 32), values)
    await createProduct(payload)
    await loadProducts()
  }

  async function handleUpdate(productId: string, values: ProductFormValues) {
    const payload = formValuesToPayload(productId, values)
    await updateProduct(productId, payload)
    await loadProducts()
  }

  async function handleDelete(productId: string) {
    try {
      await deleteProduct(productId)
      await loadProducts()
    } catch (error) {
      setError(extractErrorMessage(error, 'Nao foi possivel excluir o produto no momento.'))
    }
  }

  return {
    products,
    categories,
    totalPages,
    totalItems,
    loading,
    error,
    reload: loadProducts,
    createProduct: handleCreate,
    updateProduct: handleUpdate,
    deleteProduct: handleDelete,
    setProducts,
  }
}
