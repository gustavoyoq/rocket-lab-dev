export interface Product {
  id_produto: string
  nome_produto: string
  categoria_produto: string
  imagem_url: string | null
  peso_produto_gramas: number | null
  comprimento_centimetros: number | null
  altura_centimetros: number | null
  largura_centimetros: number | null
}

export interface ProductInput {
  id_produto: string
  nome_produto: string
  categoria_produto: string
  imagem_url: string | null
  peso_produto_gramas: number | null
  comprimento_centimetros: number | null
  altura_centimetros: number | null
  largura_centimetros: number | null
}

export interface ProductFormValues {
  nome_produto: string
  categoria_produto: string
  imagem_url: string
  peso_produto_gramas: string
  comprimento_centimetros: string
  altura_centimetros: string
  largura_centimetros: string
}

export interface OrderItem {
  id_pedido: string
  id_item: number
  id_produto: string
  id_vendedor: string
  preco_BRL: number
  preco_frete: number
}

export interface ProductReview {
  id_avaliacao: string
  id_pedido: string
  avaliacao: number
  titulo_comentario: string | null
  comentario: string | null
  data_comentario: string | null
  data_resposta: string | null
}

export interface ProductListingItem extends Product {
  salesCount: number
  averageRating: number
  reviewCount: number
}

export interface ProductListApiItem extends Product {
  sales_count: number
  average_rating: number
  review_count: number
}

export interface ProductPaginationApiResponse {
  items: ProductListApiItem[]
  page: number
  page_size: number
  total_items: number
  total_pages: number
}

export interface ProductPaginationResponse {
  items: ProductListingItem[]
  page: number
  pageSize: number
  totalItems: number
  totalPages: number
}

export interface ProductDetailsApiResponse extends Product {
  sales_count: number
  average_rating: number
  review_count: number
}

export interface ProductReviewsPaginationApiResponse {
  items: ProductReview[]
  page: number
  page_size: number
  total_items: number
  total_pages: number
}
