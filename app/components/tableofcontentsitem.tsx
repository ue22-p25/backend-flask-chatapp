// https://github.com/Jon-Peppinck/nextjsblog/blob/main/components/TableOfContentsItem.component.tsx

'use client'

import { FC, ReactNode } from 'react'

interface Props {
  topic: string
  children: ReactNode
}

const TableOfContentsItem: FC<Props> = ({ topic, children }) => {
  const label = topic.replace('step ', '')
  return (
    // keep as is
    <section id={label} className='section-heading'>
      <h2>{topic}</h2>
      <div>{children}</div>
    </section>
  )
}

export default TableOfContentsItem

