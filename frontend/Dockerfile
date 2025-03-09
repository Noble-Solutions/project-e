# Этап сборки (общий для dev и prod)
FROM node:20-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

# Этап разработки (dev)
FROM node:20-alpine AS dev

WORKDIR /app

COPY --from=build /app .

EXPOSE 5173

CMD ["npm", "run", "dev", "--host"]

# Этап продакшена (prod)
FROM node:20-alpine AS prod

WORKDIR /app

COPY --from=build /app .

RUN npm run build

RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "build", "-l", "3000"]