USE [Test2]
GO

/****** Создание таблиц для анализа данных из hh.ru     Script Date: 14.11.2023 23:00:16 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[t_skills](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[vacancy] [int] NULL,
	[skill] [nvarchar](250) NULL,
 CONSTRAINT [PK_t_skills] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

CREATE TABLE [dbo].[t_salary](
	[id] [bigint] IDENTITY(1,1) NOT NULL,
	[vac_id] [int] NULL,
	[salary] [int] NULL,
	[salary_cur] [nchar](10) NULL,
	[salary_from] [int] NULL,
	[salary_to] [int] NULL,
	[Netto_brutto] [nchar](10) NULL,
 CONSTRAINT [PK_t_salary] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

CREATE TABLE [dbo].[t_vacancies](
	[id] [bigint] NOT NULL,
	[name] [nvarchar](250) NULL,
	[description] [nvarchar](max) NULL,
	[salary] [nchar](50) NULL,
	[alternate_url] [nchar](250) NULL,
	[employer_name] [nchar](250) NULL,
	[employer_id] [int] NULL,
	[created_at] [nchar](50) NULL,
	[created_date] [date] NULL,
	[schedule] [nchar](50) NULL,
	[create_row] [smalldatetime] NULL,
 CONSTRAINT [PK_t_vacancies] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

GO

ALTER TABLE [dbo].[t_vacancies] ADD  CONSTRAINT [DF_t_vacancies_create_row]  DEFAULT (getdate()) FOR [create_row]
GO
