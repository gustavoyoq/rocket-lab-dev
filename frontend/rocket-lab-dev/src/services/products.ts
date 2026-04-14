import { api } from './api'
import type {
  ProductDetailsApiResponse,
  Product,
  ProductInput,
  ProductListingItem,
  ProductPaginationApiResponse,
  ProductPaginationResponse,
  ProductReview,
  ProductReviewsPaginationApiResponse,
} from '../types/product'

interface ListProductsParams {
  page: number
  pageSize: number
  search?: string
  category?: string
  ratingSort?: 'none' | 'asc' | 'desc'
  salesSort?: 'none' | 'asc' | 'desc'
}

export async function listProducts(params: ListProductsParams): Promise<ProductPaginationResponse> {
  const response = await api.get<ProductPaginationApiResponse>('/produtos', {
    params: {
      page: params.page,
      page_size: params.pageSize,
      search: params.search?.trim() || undefined,
      categoria: params.category && params.category !== 'all' ? params.category : undefined,
      sort_rating: params.ratingSort,
      sort_sales: params.salesSort,
    },
  })

  return {
    items: response.data.items.map((item) => ({
      ...item,
      salesCount: item.sales_count,
      averageRating: item.average_rating,
      reviewCount: item.review_count,
    })),
    page: response.data.page,
    pageSize: response.data.page_size,
    totalItems: response.data.total_items,
    totalPages: response.data.total_pages,
  }
}

export async function listProductCategories(): Promise<string[]> {
  const response = await api.get<string[]>('/produtos/categorias')
  return response.data
}

export async function getProductById(productId: string): Promise<Product> {
  const response = await api.get<Product>(`/produtos/${productId}`)
  return response.data
}

export async function getProductDetailsById(productId: string): Promise<ProductListingItem> {
  const response = await api.get<ProductDetailsApiResponse>(`/produtos/${productId}/detalhes`)
  return {
    ...response.data,
    salesCount: response.data.sales_count,
    averageRating: response.data.average_rating,
    reviewCount: response.data.review_count,
    estimatedPriceBrl: response.data.estimated_price_brl,
  }
}

interface ListProductReviewsByIdParams {
  page: number
  pageSize: number
}

export async function listProductReviewsById(
  productId: string,
  params: ListProductReviewsByIdParams,
): Promise<ProductReview[]> {
  const response = await api.get<ProductReviewsPaginationApiResponse>(`/produtos/${productId}/avaliacoes`, {
    params: {
      page: params.page,
      page_size: params.pageSize,
    },
  })

  return response.data.items
}

export async function createProduct(payload: ProductInput): Promise<Product> {
  const response = await api.post<Product>('/produtos', payload)
  return response.data
}

export async function updateProduct(productId: string, payload: Partial<ProductInput>): Promise<Product> {
  const response = await api.patch<Product>(`/produtos/${productId}`, payload)
  return response.data
}

export async function deleteProduct(productId: string): Promise<void> {
  await api.delete(`/produtos/${productId}`)
}
