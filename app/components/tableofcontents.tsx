// https://github.com/Jon-Peppinck/nextjsblog/blob/main/components/TableOfContents.component.tsx

'use client'

import { FC, useState, useEffect } from 'react'

import Timeline from '@mui/lab/Timeline'
import TimelineItem from '@mui/lab/TimelineItem'
import TimelineContent from '@mui/lab/TimelineContent'
import TimelineDot from '@mui/lab/TimelineDot'

interface Props {}

interface Section {
  topic: string
  boundingTop: number
  isActive: boolean
}

const marginTop = 100

const TableOfContents: FC<Props> = () => {
  const [offsetY, setOffsetY] = useState(0)
  const [sections, setSections] = useState<Section[]>([])

  // const customTheme = useTheme()

  useEffect(() => {
    window.scrollTo(0, 0)
    setOffsetY(0)
  }, [])

  useEffect(() => {
    const els: HTMLElement[] = Array.from(
      document.querySelectorAll('section.section-heading')
    )

    const allSections = els.map((el: HTMLElement, index: number) => {
      const { top: boundingTop } = el.getBoundingClientRect()

      return {
        topic: el.getAttribute('id')!,
        boundingTop,
        isActive: index === 0,
      }
    })

    setSections(allSections)
  }, [])

  useEffect(() => {
    if (sections.length <= 1) return

    const onScroll = () => {
      setOffsetY(window.pageYOffset)
    }
    window.addEventListener('scroll', onScroll)

    return () => window.removeEventListener('scroll', onScroll)
  }, [sections])

  useEffect(() => {
    if (sections.length === 0) return

    if (sections.length === 1) {
      sections[0].isActive = true
      return
    }

    sections.forEach((section: Section, index: number) => {
      if (index === 0) {
        section.isActive =
          sections[index + 1].boundingTop > offsetY + marginTop
      } else {
        if (sections[index + 1]) {
          section.isActive =
            sections[index + 1].boundingTop > offsetY + marginTop &&
            sections[index].boundingTop <= offsetY + marginTop
        } else {
          section.isActive = sections[index].boundingTop <= offsetY + marginTop
        }
      }
    })
  }, [sections, offsetY])

  return (
    <div style={{ position: 'fixed', top: 40, right: 0, width: 'inherit' }}>
      <Timeline position="right">
        {sections?.map((section: Section, index: number) => {
          return (
            <TimelineItem key={index}>
              <TimelineDot
                color='secondary'
                variant={section.isActive ? 'filled' : 'outlined'}
              />
              <TimelineContent>
                <span
                  onClick={() => {
                    window.scrollTo(0, section.boundingTop - marginTop)
                    setOffsetY(section.boundingTop - marginTop)
                  }}
                  style={{
                    textDecoration: 'none',
                    // color: section.isActive
                    //   ? customTheme.palette.secondary.main
                    //   : customTheme.palette.text.primary,
                    color: section.isActive ? 'goldenrod' : 'var(--color-pink)',
                    // textTransform: 'capitalize',
                    cursor: 'pointer',
                  }}
                >
                  {section.topic}
                </span>
              </TimelineContent>
            </TimelineItem>
          )
        })}
      </Timeline>
    </div>
  )
}

export default TableOfContents